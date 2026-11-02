; RICOS SOUND ODYSSEY - TEST68 - LFO cooperative service while FIRE held
; This block reuses memory retired with TEST65B's menu at $0B0E.
; It does NOT disable sprite hardware, alter the SID engine or hook an IRQ.
; Implementation is experimental; observe modulation under VICE PAL.
;
; Two original call-sites are redirected by the companion builder:
;   $3A27: INY/BNE $3A27  -> JSR lfo_wait_256  (waits exactly 256 Y steps)
;   $38A0: LDA $38FF      -> JSR lfo_input_scan (returns exact LDA $38FF)
;
; $0BFE = once-per-frame latch; $0BFF = reentrancy lock (both zero initially)
; Service uses raster line 0..63 only when high bit of $D011 is clear,
; so a line window is visited once per PAL frame (not twice at line 256).
;
* = $0B0E
lfo_wait_256:
  iny
  bne lfo_wait_256
  jsr lfo_service
  rts

lfo_input_scan:
  txa
  pha
  tya
  pha
  jsr lfo_service
  pla
  tay
  pla
  tax
  lda $38FF
  rts

lfo_service:
  pha
  txa
  pha
  tya
  pha
  bit $D011
  bmi lfo_outside_window
  lda $D012
  cmp #$40
  bcs lfo_outside_window
  lda $0BFE
  bne lfo_finish
  lda #$01
  sta $0BFE
  lda $0BFF
  bne lfo_finish
  lda #$01
  sta $0BFF
  jsr $468F
  lda #$00
  sta $0BFF
  jmp lfo_finish
lfo_outside_window:
  lda #$00
  sta $0BFE
lfo_finish:
  pla
  tay
  pla
  tax
  pla
  rts
