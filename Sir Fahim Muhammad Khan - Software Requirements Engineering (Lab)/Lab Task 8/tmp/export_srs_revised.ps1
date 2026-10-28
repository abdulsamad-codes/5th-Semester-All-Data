$ErrorActionPreference = 'Stop'
$srsRoot = Split-Path -Parent $PSScriptRoot
$srsWord = New-Object -ComObject Word.Application
$srsWord.Visible = $false
$srsWord.DisplayAlerts = 0
try {
    $srsDoc = $srsWord.Documents.Open((Join-Path $srsRoot 'output\Enterprise RAG Assistant SRS Revised.docx'))
    $srsDoc.UpdateStylesOnOpen = $false
    foreach ($srsStyleName in @('Title','Subtitle','Heading 1','Heading 2','Heading 3','Heading 4','Contents Heading')) {
        $srsStyle = $srsDoc.Styles.Item($srsStyleName)
        $srsStyle.Font.Name = 'Times New Roman'
        $srsStyle.Font.Color = 0
        $srsStyle.Borders.Enable = 0
    }
    $srsDoc.Styles.Item('Subtitle').Font.Italic = 0
    $srsDoc.Fields.Update() | Out-Null
    foreach ($srsToc in $srsDoc.TablesOfContents) { $srsToc.Update() }
    foreach ($srsStyleName in @('TOC 1','TOC 2','TOC 3')) {
        $srsStyle = $srsDoc.Styles.Item($srsStyleName)
        $srsStyle.Font.Name = 'Times New Roman'
        $srsStyle.Font.Size = 10.5
        $srsStyle.Font.Color = 0
        $srsStyle.ParagraphFormat.SpaceAfter = 3
    }
    $srsDoc.Repaginate()
    foreach ($srsToc in $srsDoc.TablesOfContents) { $srsToc.UpdatePageNumbers() }
    $srsDoc.Save()
    $srsDoc.ExportAsFixedFormat((Join-Path $srsRoot 'output\Enterprise RAG Assistant SRS Revised.pdf'),17)
    Write-Output ('Pages: ' + $srsDoc.ComputeStatistics(2))
    $srsDoc.Close(0)
} finally {
    $srsWord.Quit()
}

