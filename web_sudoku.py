from __future__ import annotations

import json
import os
import random
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import List, Tuple
from urllib.parse import parse_qs, urlparse

from sudoku import generate_puzzle

BASE_DIR = Path(__file__).parent


def clamp_clues(value: int) -> int:
    return max(17, min(81, value))


class SudokuHandler(SimpleHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802 (matching parent signature)
        parsed = urlparse(self.path)
        if parsed.path == "/api/new":
            self.handle_new(parsed.query)
            return

        if parsed.path == "/":
            self.path = "/web_index.html"
        return super().do_GET()

    def handle_new(self, query: str) -> None:
        params = parse_qs(query)
        clues = clamp_clues(int(params.get("clues", [32])[0]))
        seed_param = params.get("seed", [None])[0]
        if seed_param is not None:
            try:
                random.seed(int(seed_param))
            except ValueError:
                pass

        puzzle, solution = generate_puzzle(clues)
        givens: List[Tuple[int, int]] = [
            (r, c) for r in range(9) for c in range(9) if puzzle[r][c]
        ]
        payload = json.dumps(
            {"puzzle": puzzle, "solution": solution, "givens": givens},
            ensure_ascii=False,
        ).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


if __name__ == "__main__":
    os.chdir(BASE_DIR)
    server = ThreadingHTTPServer(("0.0.0.0", 5000), SudokuHandler)
    print("ブラウザ版数独を http://localhost:5000 で提供中です。Ctrl+C で終了します。")
    server.serve_forever()
