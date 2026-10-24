# CE2407A Tutorial 3

Fifteen web slides for Tutorial 3, Week 11, covering Tutorial Questions Set 2, Q3-Q6.

1. Tutorial 3
2. Q3: Original question statement
3. Q3: Lecture notes (standard normal table)
4. Q3: Airport capacity
5. Q4: Original question statement
6. Q4: Original graphs and question parts (continued)
7. Q4: Lecture notes (lognormal distribution)
8. Q4: Annual flood risk
9. Q5: Original question statement
10. Q5: Lecture notes (Poisson process)
11. Q5: Stations and fuel range
12. Q6: Original question statement
13. Q6: Lecture notes (exponential distribution)
14. Q6: Lock cycle and waiting
15. Blank whiteboard for handwritten equations

## Present

Open [the presentation](https://jiaruilei.github.io/CE2407A-Tutorial3-Slides/). Use the arrow keys or bottom buttons to change slides. Press O for overview and F for full screen. When a question has keyboard focus, use the bottom buttons to change slides.

The top question menu jumps directly to **Question**, **Notes** or **Explore** for Set 2 Q3, Q4, Q5 and Q6. Its active item follows arrow navigation and browser history. **Open exercise** opens the current question in the responsive tutorial in a new tab, with normal-sized controls on phones. These study controls stay outside the scaled slides.

Phones retain the same slide layout and navigation. Rotate to landscape for larger text, or use **View larger** on a question statement or lecture-notes page to open its image viewer. Drag or scroll to pan, use the zoom buttons or select **Fit width**, then **Close** to return. The viewer preserves all crop proportions and leaves slide annotations intact. Reveal's automatic mobile scroll view is disabled because it reparents slides and breaks this deck's fixed layout and annotation surfaces.

Full screen uses the browser's standard or WebKit fullscreen API when available. If the browser does not support or allow it, **Expand view** uses the available browser window with compact controls. Select **Exit view** to return. On wide screens the controls move beside the slide to leave its full height available. The browser may keep its address bar visible. This mode does not claim to bypass that browser restriction.

Interactive slides use a larger panel with a compact heading. **Enlarge exercise** fills the slide, and **Back to slide** restores its layout. **More → Reset exercise** reloads only that exercise and clears its answers and chat. Leaving a slide preserves its calculations and chat.

The live exercises need an internet connection. All four embed [CE2407A_Tutorial2](https://jiaruilei.github.io/CE2407A_Tutorial2/), using `question=q3`, `question=q4`, `question=q5` or `question=q6` and `embed=1`. The existing app provides calculations, MathJax and AI coaching. No API keys belong in this repository.

## Annotate

The final slide is a blank whiteboard. Reach it with the next-slide button after T2 Q6, or choose **Whiteboard** from the top menu. Select **Ink** to write equations. It supports the same pen, highlighter, eraser, undo/redo and automatic saving as the other slides.

Select **Ink** in the bottom controls to open the annotation toolbar. Use Pen or Highlighter with a classroom pen, mouse or touch input. Choose a color and thickness. Eraser removes a whole stroke. Undo, Redo and Clear ink apply to the current slide view. Clearing is undoable.

Choose **Pointer** or press Escape to interact with the question. Ink drawn over the embedded question follows its main page as you scroll. Scrolling inside the chat or other nested panels, and opening content that changes the layout, does not reposition existing ink. Normal and expanded layouts keep separate ink because the question reflows when expanded. Full screen and window resizing preserve alignment. Ink remains visible when the toolbar is closed.

Ink is saved automatically in this browser on this device, under its own Tutorial 3 namespace, separate from Tutorial 1 and Tutorial 2. It is not synced to GitHub or other computers. Use one presentation tab when annotating the same slide. If browser storage is unavailable, ink remains available while the tab stays open. Ctrl+Z undoes ink and Ctrl+Y (or Ctrl+Shift+Z) redoes it while the toolbar is open. Text fields retain normal editing shortcuts.

The pen must send normal pen, mouse or touch input to the browser. This feature does not capture webcam video or require camera permission. Test the classroom device before teaching.

Run `npm test` with Node.js to check annotation history, storage validation, coordinate scaling and stroke erasing.

## Design and assets

The 1280 × 720 layout, navy and orange palette, Arial type, title positions, question snapshot scale, embedded panels and controls match [CE2407A-Tutorial1-Slides](https://github.com/jiaruilei/CE2407A-Tutorial1-Slides). The question, cover and exercise layouts retain their original styling. The question menu also includes Notes links. The cover QR code links to this deck and includes a four-module quiet zone. Reveal.js is bundled with its license in `LICENSE-reveal.txt`.

Question statements and diagrams are cropped from the supplied `CE2407A Tutorial Questions Set 2.pdf` (pages 2, 3, 4, Q3-Q6). Each crop is rendered at 288 dpi and displayed at 2 CSS pixels per PDF point, matching Tutorial 1. Titles stay at x=97.92, y=32, with 52px Arial type. Question text starts at x=98, y=132. Cropped parts retain their original scale when rearranged to fit a slide.

Q4 uses a continuation slide to preserve the original text size and the diagrams' left/right arrangement.

`assets/questions/manifest.json` records source PDF checksums, page numbers, crop bounds, display dimensions and positions. To rebuild the snapshots, run `python scripts/extract-questions.py --help` for the required PDF path. The original PDF is not included in this repository.

The statement IDs are `question-t2-q3`, `question-t2-q4`, `question-t2-q4-continued`, `question-t2-q5` and `question-t2-q6`. Cover and explore IDs are `slide-1` through `slide-5`; the final blank slide is `whiteboard`. Keep these IDs and the ink namespace stable when editing content.

## Lecture-note snapshots

The four lecture-note snapshots come from slides 3, 8, 13 and 18 of the supplied `Tutorial 3_Recorded.pptx`. The original PNG images are extracted without re-encoding. The lognormal, Poisson and exponential snapshots each contain two stacked panels, shown side by side on their notes page. The normal table is split between row ranges, with its original header repeated above the second range. All content and annotations baked into the source images are retained.

`assets/lecture-notes/manifest.json` records the PowerPoint checksum, original media members, panel bounds and displayed positions. Run `python scripts/extract-lecture-notes.py --help` to rebuild these assets from the supplied PowerPoint. The PowerPoint itself is not included in the repository.

The notes IDs are `notes-t2-q3` through `notes-t2-q6`. They share the existing ink tools and image viewer, with separate saved ink per page. Existing slide IDs and the storage namespace are unchanged.

## Local preview

Run `python -m http.server 4173` in this directory and open [http://localhost:4173](http://localhost:4173). Local previews can use the live exercises, but ink anchored to scrolling inside an exercise requires the same origin. The published slide and exercise sites share the same GitHub Pages origin. Run `npm test` to check ink persistence and fullscreen behavior.

## Publish

GitHub Pages serves the repository root from the main branch. No build step is required. Edit `index.html`, `styles.css` or `presentation.js` and push to main to update the slides.

