---
description: Fast condensed corporate check on a publicly listed company — business summary, top 2 strengths, top 2 concerns, and an overall verdict in under 60 seconds. Use when the user wants a quick read on a company rather than the full CorpDNA report.
---

# CorpDNA — Quick Check

If no company name is given in `$ARGUMENTS`, respond with exactly:

"Give me a publicly listed company name and I will run a quick check.
Example: /corpdna:quick-check Infosys
Example: /corpdna:quick-check HDFC Bank"

Otherwise, invoke the `corpdna` subagent with the company name `$ARGUMENTS`
and ask it to run a condensed analysis. The subagent should return only:

1. One paragraph — what the company does and how it makes money
2. Top 2 strengths found
3. Top 2 concerns or red flags found
4. One sentence overall verdict (STRONG / MIXED / WEAK profile)

Label the output "QUICK CHECK" clearly. Tell the user to run
`/corpdna:analyze` for the full five-dimension report.
