#!/usr/bin/env python3
"""Prepare fixed-bank PSID staging assets for SIDPLAY64MIX TEST01.

This tool never modifies the input disk.  It prepares only PSID tunes with
INIT=$1000, PLAY=$1003, one subtune and a payload <=8192 bytes.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

TRACK_SECTORS = tuple([0] + [21]*17 + [19]*7 + [18]*6 + [17]*5)
STAGE_START = 0x5000
STAGE_CAPACITY = 0x2000
EXEC_START = 0x1000
EXEC_CAPACITY = 0x2000


def sector_offset(track: int, sector: int) -> int:
    if not (1 <= track <= 35 and 0 <= sector < TRACK_SECTORS[track]):
        raise ValueError(f"invalid D64 sector T{track} S{sector}")
    return (sum(TRACK_SECTORS[:track]) + sector) * 256


def read_chain(disk: bytes, track: int, sector: int) -> bytes:
    parts: list[bytes] = []
    visited = set()
    while track:
        if (track, sector) in visited:
            raise ValueError("D64 file chain is cyclic")
        visited.add((track, sector))
        p = sector_offset(track, sector)
        chunk = disk[p:p+256]
        if len(chunk) != 256:
            raise ValueError("truncated D64")
        next_track, next_sector = chunk[:2]
        used = 254 if next_track else next_sector - 1
        if not (0 <= used <= 254):
            raise ValueError("malformed last D64 sector")
        parts.append(chunk[2:2+used])
        track, sector = next_track, next_sector
    return b"".join(parts)


def entries(disk: bytes) -> list[dict]:
    if len(disk) not in (174848, 175531):
        raise ValueError("expected 35-track D64 with or without error bytes")
    track, sector = 18, 1
    visited = set()
    result = []
    while track:
        if (track, sector) in visited:
            raise ValueError("cyclic directory")
        visited.add((track, sector))
        off = sector_offset(track, sector)
        page = disk[off:off+256]
        next_track, next_sector = page[0], page[1]
        for i in range(8):
            entry = page[i*32+2:(i+1)*32]
            if len(entry) != 30 or entry[0] & 0x83 != 0x82:
                continue
            filename = entry[3:19].replace(b"\xa0", b" ").decode("latin1").strip()
            result.append({"filename": filename, "data": read_chain(disk, entry[1], entry[2])})
        track, sector = next_track, next_sector
    return result


def psid_record(filename: str, blob: bytes) -> dict:
    if len(blob) < 124 or blob[:4] != b"PSID":
        raise ValueError(f"{filename}: expected PSID header")
    def be16(off: int) -> int:
        return int.from_bytes(blob[off:off+2], "big")
    offset, address, init, play, songs = (be16(x) for x in (6, 8, 10, 12, 14))
    if not (124 <= offset <= len(blob)):
        raise ValueError(f"{filename}: invalid PSID data offset")
    payload = blob[offset:]
    if address == 0:
        if len(payload) < 2:
            raise ValueError(f"{filename}: missing load address")
        address = int.from_bytes(payload[:2], "little")
        payload = payload[2:]
    if not (address == EXEC_START and init == EXEC_START and play == EXEC_START + 3):
        raise ValueError(f"{filename}: unsupported addresses for TEST01")
    if songs != 1 or not (0 < len(payload) <= min(STAGE_CAPACITY, EXEC_CAPACITY)):
        raise ValueError(f"{filename}: unsupported subtunes or size")
    speed = int.from_bytes(blob[18:22], "big")
    flags = be16(118) if len(blob) >= 120 else 0
    return {"filename": filename, "load_address": address,
            "init_address": init, "play_address": play,
            "subtunes": songs, "speed_bits": f"{speed:08X}",
            "psid_flags": f"{flags:04X}", "length": len(payload),
            "sha256": hashlib.sha256(payload).hexdigest(), "payload": payload}


def prepare(d64: Path, output: Path, picks: tuple[int, ...]) -> None:
    found = entries(d64.read_bytes())
    sids = [e for e in found if e["data"].startswith(b"PSID")]
    print(f"{len(sids)} PSID files found in {d64.name}")
    if not picks:
        for i, item in enumerate(sids, 1):
            try:
                r = psid_record(item["filename"], item["data"])
                print(f"{i:2} {r['filename']:19} {r['length']:5} bytes  ${r['load_address']:04X}  speed={r['speed_bits']}")
            except ValueError as error:
                print(f"{i:2} unsupported: {error}")
        return
    if len(picks) != 3 or len(set(picks)) != 3:
        raise ValueError("choose three different 1-based PSID positions: --tracks A B C")
    if any(i < 1 or i > len(sids) for i in picks):
        raise ValueError("PSID position out of range")
    records = [psid_record(sids[i-1]["filename"], sids[i-1]["data"]) for i in picks]
    if len({r["speed_bits"] for r in records}) != 1:
        raise ValueError("TEST01 requires identical speed bits")
    output.mkdir(parents=True, exist_ok=True)
    manifest = {"test": "SIDPLAY64MIX_TEST01_ASSET_STAGING",
                "status": "ASSETS_ONLY_NOT_RUNTIME_PASS",
                "stage_window": "$5000-$6FFF", "exec_window": "$1000-$2FFF",
                "loader": "KrillLoad integration not implemented yet", "tracks": []}
    for slot, record in zip("ABC", records):
        addr = EXEC_START if slot == "A" else STAGE_START
        filename = f"MIX_{slot}.PRG"
        (output / filename).write_bytes(addr.to_bytes(2, "little") + record["payload"])
        manifest["tracks"].append({k: v for k, v in record.items() if k != "payload"} |
                                  {"slot": slot, "carrier": filename, "carrier_address": f"${addr:04X}"})
        print(f"{slot}: {record['filename']} -> {filename} at ${addr:04X} ({record['length']} bytes)")
    (output / "TEST01_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Created: {output / 'TEST01_MANIFEST.json'}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("d64", type=Path)
    parser.add_argument("--output", type=Path, default=Path("build/test01"))
    parser.add_argument("--tracks", nargs=3, type=int, metavar=("A", "B", "C"))
    args = parser.parse_args()
    prepare(args.d64, args.output, tuple(args.tracks or ()))


if __name__ == "__main__":
    main()
