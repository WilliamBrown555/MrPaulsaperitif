# Mr. Paul's Apéritif & Digestif List

This repo is a publish target. Netlify serves `Aperitif Website/` with an empty build
command, so what is committed here is what is live.

**Nothing here is edited by hand.** The source lives one folder up, in
`Documents/Mr. Pauls/Menu Build/menus/`. To change this page:

```
cd ../menus
python build.py aperitif      # or just `python build.py` for all of them
```

then commit the rebuilt file here and push. The push is the deploy.

Before pushing, `python build.py --check` will tell you whether the
committed file still matches a fresh build.
