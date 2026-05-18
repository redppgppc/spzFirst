"""
PLY property 순서를 PlayCanvas/SPZ 친화 레이아웃에서 INRIA 표준 순서로 재정렬.

입력 가정 (PlayCanvas splat-transform / SuperSplat Save As):
  x, y, z,
  scale_0..2, f_dc_0..2, opacity, rot_0..3, f_rest_0..44

출력 (INRIA Gaussian Splatting reference):
  x, y, z,
  f_dc_0..2, f_rest_0..44, opacity, scale_0..2, rot_0..3

값 자체는 보존, 헤더 + binary 레이아웃만 재배열.
"""
import sys
import numpy as np
from pathlib import Path

INPUT = Path(r"D:\Temp\plyTest_5_3_2\Content\StarterContent\Ply\test_savedas.ply")
OUTPUT = Path(r"D:\Temp\plyTest_5_3_2\Content\StarterContent\Ply\test_inria_ordered.ply")


def parse_header(path):
    header_bytes = bytearray()
    with open(path, "rb") as f:
        while True:
            line = f.readline()
            if not line:
                raise RuntimeError("end_header not found")
            header_bytes += line
            if line.startswith(b"end_header"):
                break
        binary_offset = f.tell()

    header_str = header_bytes.decode("ascii")
    vertex_count = None
    properties = []
    for line in header_str.split("\n"):
        s = line.strip()
        if s.startswith("element vertex"):
            vertex_count = int(s.split()[-1])
        elif s.startswith("property float"):
            properties.append(s.split()[-1])
        elif s.startswith("format") and "binary_little_endian" not in s:
            raise RuntimeError(f"Expected binary_little_endian, got: {s}")
    if vertex_count is None:
        raise RuntimeError("vertex count not found")
    return vertex_count, properties, binary_offset


def main():
    if not INPUT.exists():
        print(f"ERROR: input not found: {INPUT}", file=sys.stderr)
        sys.exit(1)

    print(f"Reading header: {INPUT}")
    vcount, props, off = parse_header(INPUT)
    print(f"  vertex_count = {vcount:,}")
    print(f"  properties   = {len(props)} props, offset = {off}")
    print(f"  first 6 props: {props[:6]}")

    target = (
        ["x", "y", "z"]
        + [f"f_dc_{i}" for i in range(3)]
        + [f"f_rest_{i}" for i in range(45)]
        + ["opacity"]
        + [f"scale_{i}" for i in range(3)]
        + [f"rot_{i}" for i in range(4)]
    )

    missing = [p for p in target if p not in props]
    if missing:
        print(f"ERROR: input missing required INRIA properties: {missing}", file=sys.stderr)
        sys.exit(2)

    if len(props) != len(target):
        extras = [p for p in props if p not in target]
        print(f"WARNING: input has extra props not in target: {extras}", file=sys.stderr)

    src_idx = np.array([props.index(p) for p in target], dtype=np.int32)
    n_in = len(props)
    n_out = len(target)

    print(f"  loading {vcount * n_in * 4 / 1024 / 1024:.1f} MB via memmap")
    arr = np.memmap(INPUT, dtype="<f4", mode="r", offset=off, shape=(vcount, n_in))

    new_header = (
        "ply\n"
        "format binary_little_endian 1.0\n"
        f"element vertex {vcount}\n"
        + "".join(f"property float {p}\n" for p in target)
        + "end_header\n"
    ).encode("ascii")

    print(f"Writing: {OUTPUT}")
    print(f"  new header size: {len(new_header)} bytes")
    print(f"  new payload size: {vcount * n_out * 4 / 1024 / 1024:.1f} MB")

    with open(OUTPUT, "wb") as f:
        f.write(new_header)
        chunk = 200_000
        for start in range(0, vcount, chunk):
            end = min(start + chunk, vcount)
            block = np.ascontiguousarray(arr[start:end, src_idx], dtype="<f4")
            block.tofile(f)
            if start % (chunk * 5) == 0:
                pct = 100 * end / vcount
                print(f"    {end:,} / {vcount:,} ({pct:.1f}%)")

    print(f"Done. Wrote {OUTPUT.stat().st_size / 1024 / 1024:.1f} MB")


if __name__ == "__main__":
    main()
