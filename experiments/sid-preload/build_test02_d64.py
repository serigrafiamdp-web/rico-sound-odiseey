#!/usr/bin/env python3
"""Create a standard 35-track D64 containing the TEST02 harness and 3 SID PRGs.

The input PRGs must contain a 2-byte CBM load address.  This writer does not
modify any of the original files.  Single-directory-block prototype: 6 files.
"""
from pathlib import Path
import argparse, hashlib

SECTORS=[0]+[21]*17+[19]*7+[18]*6+[17]*5
assert len(SECTORS)==36 and sum(SECTORS)==683

def offset(t,s):
    assert 1<=t<=35 and 0<=s<SECTORS[t]
    return (sum(SECTORS[:t])+s)*256

def build(files,title="SIDPLAY64 MIX"):
    if not (1<=len(files)<=8):
        raise ValueError("single-directory-block format supports 1..8 files")
    data=bytearray(174848)
    used={(18,0),(18,1)}
    free=[(t,s) for t in list(range(1,18))+list(range(19,36))
          for s in range(SECTORS[t])]
    dr=offset(18,1)
    bam=offset(18,0)
    data[dr:dr+2]=bytes((0,255))
    data[bam:bam+4]=bytes((18,1,0x41,0))
    data[bam+0x90:bam+0xa0]=title.upper().encode()[:16].ljust(16,b"\xa0")
    data[bam+0xa0:bam+0xa2]=b"\xa0\xa0"
    data[bam+0xa2:bam+0xa4]=b"02"
    data[bam+0xa4]=0xa0
    data[bam+0xa5:bam+0xa7]=b"2A"
    for i,(name,blob) in enumerate(files):
        if len(blob)<3 or len(name)>16 or not name.isascii():
            raise ValueError(f"invalid name or PRG: {name}")
        required=(len(blob)+253)//254
        if len(free)<required:
            raise ValueError("disk full")
        chain=[free.pop(0) for _ in range(required)]
        for j,(t,s) in enumerate(chain):
            used.add((t,s))
            at=offset(t,s)
            chunk=blob[j*254:(j+1)*254]
            data[at:at+2]=bytes(chain[j+1]) if j+1<len(chain) else bytes((0,len(chunk)+1))
            data[at+2:at+2+len(chunk)]=chunk
        at=dr+i*32
        data[at+2]=0x82
        data[at+3:at+5]=bytes(chain[0])
        data[at+5:at+21]=name.encode().ljust(16,b"\xa0")
        data[at+30:at+32]=required.to_bytes(2,"little")
    for t in range(1,36):
        bitmap=[0,0,0]
        count=0
        for s in range(SECTORS[t]):
            if (t,s) not in used:
                bitmap[s//8]|=1<<(s%8)
                count+=1
        data[bam+4*t:bam+4*t+4]=bytes((count,*bitmap))
    return bytes(data)

def main():
    ap=argparse.ArgumentParser()
    for name in ("main","install","resident","a","b","c"):
        ap.add_argument("--"+name,required=True,type=Path)
    ap.add_argument("--out",required=True,type=Path)
    x=ap.parse_args()
    src=[("TEST02",x.main,0x0801),("INSTA",x.install,0x6000),
         ("RESIDENT",x.resident,0x9000),("MIX_A",x.a,0x1000),
         ("MIX_B",x.b,0x5000),("MIX_C",x.c,0x5000)]
    prgs=[]
    for name,path,addr in src:
        b=path.read_bytes()
        found=int.from_bytes(b[:2],"little")
        if found!=addr:
            raise ValueError(f"{name}: expected ${addr:04x}, got ${found:04x}")
        if addr==0x0801 and len(b)>=0x1000-0x0801:
            raise ValueError("boot overlaps $1000 SID execution")
        prgs.append((name,b))
        print(f"{name} ${addr:04x} {len(b)} bytes")
    x.out.parent.mkdir(parents=True,exist_ok=True)
    d64=build(prgs)
    x.out.write_bytes(d64)
    print(f"{x.out} SHA256 {hashlib.sha256(d64).hexdigest()}")

if __name__=="__main__":
    main()
