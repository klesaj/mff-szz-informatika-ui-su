#!/usr/bin/env python3
"""Numericke overeni SZZ uloh okruhu I4 (ground truth pro vzorova reseni).

Spousti se z adresare okruhu:  python3 src/fig/verify_szz.py
Vsechny tri ulohy bez oficialniho nacrtu reseni (TLB, strankovani,
binarni soubor) + jedna s oficialnim nacrtem (heap) overujeme nezavisle.
Viz pamet szz-bez-naszku-overit-numericky.
"""

# ----------------------------------------------------------------------
# q_2023-leto-15  TLB (32b adresy, 4 MB stranky, softwarove plneny TLB)
# Polozka 32b: [31:22]VPN(10) [21:12]PFN(10) [11:4]ASID(8) [3]dirty [2]valid [1:0]rsvd
# ----------------------------------------------------------------------
def tlb():
    entries = [0x35C0C124, 0x35C0613C, 0x35C08120, 0x36005134, 0x36009128,
               0x3600D12C, 0x3640E124, 0x3640A120, 0x3640413C]
    def dec(e):
        return ((e >> 22) & 0x3FF, (e >> 12) & 0x3FF, (e >> 4) & 0xFF,
                (e >> 3) & 1, (e >> 2) & 1)
    tlb = [dec(e) for e in entries]
    ASID = 0x12
    out = {}
    for op, va in [("write", 0x35803580), ("read", 0x35CD35CD),
                   ("read", 0x36003600), ("write", 0x36403640)]:
        vpn, off = (va >> 22) & 0x3FF, va & 0x3FFFFF
        hit = next(((pfn, d) for (v, pfn, a, d, val) in tlb
                    if val == 1 and v == vpn and a == ASID), None)
        out[va] = ((hit[0] << 22) | off, hit[1]) if hit else None
    return out


# ----------------------------------------------------------------------
# q_2023-leto-17  strankovani 16b, 64B stranky, PTE 16b (bit0 = valid)
# PTE 0xFBF7 precteno z tabulky @0x1ED4 (priklady/.../strankovaci-tabulka.png)
# ----------------------------------------------------------------------
def paging():
    VA, PTE = 0x328F, 0xFBF7
    pgnum, off = VA >> 6, VA & 0x3F
    return dict(page=pgnum, off=off, pte_addr=0x1D40 + pgnum * 2,
                valid=PTE & 1, pa=(PTE & ~0x3F) | off)


# ----------------------------------------------------------------------
# q_2025-leto-02  heap first-fit, 22 B, zarovnani na 2, Size bit0 = obsazeno
# ----------------------------------------------------------------------
def heap():
    H = 22
    mem = bytearray(H)
    w16 = lambda o, v: mem.__setitem__(slice(o, o + 2), bytes((v & 0xFF, (v >> 8) & 0xFF)))
    r16 = lambda o: mem[o] | (mem[o + 1] << 8)
    firstFree = 0
    w16(0, H); w16(2, 0xFFFF)

    def alloc(payload):
        nonlocal firstFree
        need = payload + 2
        if need % 2:
            need += 1
        o = firstFree
        while o != 0xFFFF and not ((r16(o) & 1) == 0 and (r16(o) & ~1) >= need):
            o = r16(o + 2)
        sz, nxt = r16(o) & ~1, r16(o + 2)
        prev = None; p = firstFree
        while p != o:
            prev = p; p = r16(p + 2)
        if sz - need >= 4:
            w16(o + need, sz - need); w16(o + need + 2, nxt); link = o + need
        else:
            need, link = sz, nxt
        if prev is None:
            firstFree = link
        else:
            w16(prev + 2, link)
        w16(o, need | 1)
        for i in range(o + 2, o + need):
            mem[i] = 0
        return o + 2

    def free(po):
        nonlocal firstFree
        o = po - 2
        w16(o, r16(o) & ~1)
        if firstFree == 0xFFFF or o < firstFree:
            w16(o + 2, firstFree); firstFree = o; return
        p = firstFree
        while r16(p + 2) != 0xFFFF and r16(p + 2) < o:
            p = r16(p + 2)
        w16(o + 2, r16(p + 2)); w16(p + 2, o)

    A = alloc(2); B = alloc(4); C = alloc(2); free(B)
    return bytes(mem)


# ----------------------------------------------------------------------
# q_2025-podzim-02  binarni soubor, BIG-endian
# ----------------------------------------------------------------------
def binfile():
    hx = ("00 06 48 68 53 53 4C 4C 00 22 03 E8 FC 18 00 05 "
          "48 65 6C 6C 6F 00 05 57 6F 72 6C 64 00 00 00 00 "
          "00 00 00 2C 00 00 00 00 00 00 12 34 00 88 01 F4")
    b = bytes(int(x, 16) for x in hx.split())
    n = (b[0] << 8) | b[1]
    types = b[2:2 + n]
    p = 2 + n + 2
    vals = []
    for t in types:
        if t in (0x48, 0x68):
            v = (b[p] << 8) | b[p + 1]
            if t == 0x68 and v >= 0x8000:
                v -= 0x10000
            vals.append(v); p += 2
        elif t == 0x53:
            L = (b[p] << 8) | b[p + 1]
            vals.append(b[p + 2:p + 2 + L].decode("ascii")); p += 2 + L
        elif t == 0x4C:
            vals.append(int.from_bytes(b[p:p + 8], "big")); p += 8
    return vals


if __name__ == "__main__":
    print("TLB:", {hex(k): (hex(v[0]), v[1]) if v else None for k, v in tlb().items()})
    print("paging:", {k: hex(v) for k, v in paging().items()})
    h = heap()
    official = bytes.fromhex("050000000600 0E00 0000 0500 0000 0800 FFFF 00000000".replace(" ", ""))
    print("heap match:", h == official, h.hex())
    print("binfile:", binfile())
