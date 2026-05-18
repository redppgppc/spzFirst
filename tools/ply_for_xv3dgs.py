"""
INRIA 순서 PLY → XV3dGS plugin 호환 PLY 변환.

추가 작업 (binary string 검사로 발견한 plugin spec 기준):
  1. nx, ny, nz normal property 추가 (값 0).
  2. red, green, blue uchar property 추가. f_dc_0..2 SH degree 0에서 RGB로 변환.

INRIA SH→RGB 공식 (gaussian-splatting reference의 sh_utils.SH2RGB):
  color_normalized = f_dc * 0.28209479177387814 + 0.5
  color_byte = clip(color_normalized, 0, 1) * 255

입력 가정: INRIA 순서 PLY (x,y,z + f_dc + f_rest + opacity + scale + rot, 59 floats).
출력 구조 (vertex당 251 bytes = 62 floats + 3 uchar):
  x,y,z, nx,ny,nz, f_dc_0..2, f_rest_0..44, opacity, scale_0..2, rot_0..3, red,green,blue
"""
import sys
import numpy as np
from pathlib import Path

INPUT = Path(r"D:\Temp\plyTest_5_3_2\Content\StarterContent\Ply\test_inria_ordered.ply")
OUTPUT = Path(r"D:\Temp\plyTest_5_3_2\Content\StarterContent\Ply\test_xv3dgs.ply")

SH_C0 = 0.28209479177387814


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
    vcount = None
    props = []
    for line in header_str.split("\n"):
        s = line.strip()
        if s.startswith("element vertex"):
            vcount = int(s.split()[-1])
        elif s.startswith("property float"):
            props.append(s.split()[-1])
    return vcount, props, binary_offset


def main():
    if not INPUT.exists():
        print(f"ERROR: input not found: {INPUT}", file=sys.stderr)
        sys.exit(1)

    vcount, props, off = parse_header(INPUT)
    print(f"Input: {INPUT}")
    print(f"  vertex_count = {vcount:,}, properties = {len(props)}")

    idx_xyz = [props.index(p) for p in ["x", "y", "z"]]
    idx_fdc = [props.index(p) for p in ["f_dc_0", "f_dc_1", "f_dc_2"]]
    idx_frest = [props.index(f"f_rest_{i}") for i in range(45)]
    idx_opa = props.index("opacity")
    idx_scale = [props.index(p) for p in ["scale_0", "scale_1", "scale_2"]]
    idx_rot = [props.index(f"rot_{i}") for i in range(4)]

    arr = np.memmap(INPUT, dtype="<f4", mode="r", offset=off, shape=(vcount, len(props)))

    new_header = (
        "ply\n"
        "format binary_little_endian 1.0\n"
        f"element vertex {vcount}\n"
        "property float x\n"
        "property float y\n"
        "property float z\n"
        "property float nx\n"
        "property float ny\n"
        "property float nz\n"
        "property float f_dc_0\n"
        "property float f_dc_1\n"
        "property float f_dc_2\n"
        + "".join(f"property float f_rest_{i}\n" for i in range(45))
        + "property float opacity\n"
        "property float scale_0\n"
        "property float scale_1\n"
        "property float scale_2\n"
        "property float rot_0\n"
        "property float rot_1\n"
        "property float rot_2\n"
        "property float rot_3\n"
        "property uchar red\n"
        "property uchar green\n"
        "property uchar blue\n"
        "end_header\n"
    ).encode("ascii")

    rec_dtype = np.dtype([("floats", "<f4", 62), ("rgb", "u1", 3)])
    print(f"  record size = {rec_dtype.itemsize} bytes (should be 251)")
    print(f"  total payload = {vcount * rec_dtype.itemsize / 1024 / 1024:.1f} MB")

    print(f"Writing: {OUTPUT}")
    with open(OUTPUT, "wb") as f:
        f.write(new_header)
        chunk = 200_000
        for start in range(0, vcount, chunk):
            end = min(start + chunk, vcount)
            n = end - start

            fblock = np.zeros((n, 62), dtype="<f4")
            fblock[:, 0:3] = arr[start:end, idx_xyz]
            # nx, ny, nz = 0 (already zero)
            fblock[:, 6:9] = arr[start:end, idx_fdc]
            fblock[:, 9:54] = arr[start:end, idx_frest]
            fblock[:, 54] = arr[start:end, idx_opa]
            fblock[:, 55:58] = arr[start:end, idx_scale]
            fblock[:, 58:62] = arr[start:end, idx_rot]

            f_dc_vals = arr[start:end, idx_fdc].astype(np.float32)
            rgb_norm = np.clip(f_dc_vals * SH_C0 + 0.5, 0.0, 1.0)
            rgb_uchar = (rgb_norm * 255.0 + 0.5).astype(np.uint8)

            records = np.zeros(n, dtype=rec_dtype)
            records["floats"] = fblock
            records["rgb"] = rgb_uchar
            records.tofile(f)

            if start % (chunk * 5) == 0:
                pct = 100 * end / vcount
                print(f"    {end:,} / {vcount:,} ({pct:.1f}%)")

    print(f"Done. Wrote {OUTPUT.stat().st_size / 1024 / 1024:.1f} MB")


if __name__ == "__main__":
    main()
