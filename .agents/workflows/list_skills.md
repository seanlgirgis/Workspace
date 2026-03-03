---
description: List all available skills and their use
---

1. Search for all workflow files in the `.agents/workflows` directory.
2. Extract the description from the frontmatter of each file.
3. Present a formatted list of all skills to the user.

```powershell
Get-ChildItem -Path d:\Workspace\.agents\workflows\*.md | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    $description = "No description found"
    if ($content -match '(?s)description:\s*(.*?)(\r?\n|---)') {
        $description = $matches[1].Trim()
    }
    Write-Output "- **$($_.BaseName)**: $description"
}
```
