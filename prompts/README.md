# Claude Code Workflow

## QUICK START
1. Backend: `cd backend && .\venv\Scripts\Activate.ps1 && uvicorn app.main:app --reload`
2. Prompt: `code prompts/current.md` (schreiben/pasten)
3. Claude: `claude --file prompts/current.md`
4. Test: `pytest tests/`
5. Archive: `mv prompts/current.md prompts/completed/DATUM-feature.md`

## MULTI-STEP
Große Features splitten:
- `prompts/step1-backend.md`
- `prompts/step2-frontend.md`
- `prompts/step3-integration.md`

Dann nacheinander: `claude --file prompts/stepX.md`

## CHECKLIST
- [ ] Git backup
- [ ] Backend läuft
- [ ] Prompt token-optimiert
- [ ] Nach jedem Step testen

## TROUBLESHOOTING
- Claude findet Datei nicht: `pwd` prüfen (sollte KitchenHelper/ sein)
- Backend läuft nicht: `cd backend && pip install -r requirements.txt`

## STATISTICS
Track deine Token-Ersparnis in commits!
