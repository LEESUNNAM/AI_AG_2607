"""List available Typecast voices (characters) so the user can pick one.

Usage:
    python scripts/typecast_list_voices.py [--filter keyword]
"""

import argparse

from typecast_client import list_voices


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filter", default=None, help="이름에 포함된 키워드로 필터링")
    args = parser.parse_args()

    voices = list_voices()
    if args.filter:
        voices = [v for v in voices if args.filter.lower() in str(v.get("voice_name", "")).lower()]

    for v in voices:
        voice_id = v.get("voice_id", "")
        name = v.get("voice_name", "")
        model = v.get("model", "")
        emotions = v.get("emotions", [])
        print(f"{voice_id}\t{name}\t{model}\t{','.join(emotions) if emotions else '-'}")

    print(f"\n총 {len(voices)}개 보이스")


if __name__ == "__main__":
    main()
