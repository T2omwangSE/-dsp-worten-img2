# -*- coding: utf-8 -*-
"""用 plumbing 把 CZ5300 的 16 张图合成一个 commit 挂到远端 tip 上（不 rebase、不拉远端 blob）。"""
import subprocess, os, io, sys

sys.stdout.reconfigure(encoding="utf-8")
REPO = r"C:/Users/王禹/WorkBuddy/2026-09-15-11-36-34/_img2_repo"
SRC = r"C:/Users/王禹/WorkBuddy/2026-09-15-11-36-34/worten-mirakl/out/CZ5300_raw/imgs_clean"
SKUS = ["ZS-LT-0001", "ZS-LT-0002", "ZS-LT-0003", "ZS-LT-0004"]
ORDER = {
    "ZS-LT-0001": ["d", "a", "b", "c"],
    "ZS-LT-0002": ["a", "d", "c", "b"],
    "ZS-LT-0003": ["c", "b", "a", "d"],
    "ZS-LT-0004": ["b", "c", "d", "a"],
}
TIP = "12f0885fe7552c2cb43b6e848ed84ca5b45f77c7"
GH_USER = "T2omwangSE"


def run(args, **kw):
    r = subprocess.run(args, cwd=REPO, capture_output=True, text=True, **kw)
    assert r.returncode == 0, (args, r.stdout, r.stderr)
    return r.stdout.strip()


run(["git", "read-tree", TIP + "^{tree}"])
print("read-tree ok", flush=True)

n = 0
for sku in SKUS:
    for i, g in enumerate(ORDER[sku], 1):
        p = os.path.join(SRC, g + "c.jpg")
        assert os.path.getsize(p) > 1000, p
        blob = run(["git", "hash-object", "-w", p])
        path = "dsp/worten/%s/%s-%d.jpg" % (sku, sku, i)
        run(["git", "update-index", "--add", "--cacheinfo", "100644,%s,%s" % (blob, path)])
        n += 1
print("blobs added:", n, flush=True)

tree = run(["git", "write-tree"])
print("tree:", tree[:12], flush=True)
commit = run(["git", "commit-tree", tree, "-p", TIP, "-m",
              "img push 1109: CZ5300 sunrise wake-up light 4 sku x 4 img (ZS-LT x4)",
              "-c", "user.name=" + GH_USER, "-c", "user.email=%s@users.noreply.github.com" % GH_USER])
print("commit:", commit[:12], flush=True)
with io.open(os.path.join(REPO, "new_commit.txt"), "w") as f:
    f.write(commit)
print("saved new_commit.txt", flush=True)
