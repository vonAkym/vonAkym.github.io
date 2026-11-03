# tools

Generators for the study hub. They write finished HTML into the repo root, which GitHub Pages serves.

```
python3 tools/build_hub.py      # index.html (hub)
python3 tools/build_notes.py    # cmt322/index.html
python3 tools/build_cst435.py   # cst435/index.html
```

Python 3 only, no packages needed.

| File | Used by | Purpose |
|---|---|---|
| `build_hub.py` | hub | Hub page: its own CSS and JS are inside the script |
| `build_notes.py` | CMT322 | CMT322 notes page (contains its own content and mind-map helper) |
| `build_cst435.py` | CST435 | CST435 notes page (content for all five topics) |
| `notes_lib.py` | CST435 | Shared helpers: `mindmap`, `terms`, `psn`, `qa`, `week` |
| `style.css` | both notes pages | Notebook look, topic colours, mind maps, flashcards |
| `extra_cst.css` | CST435 | Timelines, bars, layers, Flynn grid, calculator and similar components |
| `bigp.css` | both notes pages | The "Big picture" section at the top of each page |
| `script.js` | both notes pages | Flashcards flip and the image lightbox |

Running a builder rewrites its page completely, so never hand-edit the generated HTML. See `CLAUDE.md` in the repo root for the rules and the checklist before pushing.
