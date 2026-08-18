# -*- coding: utf-8 -*-
# OpenCode Go 用量弹窗脚本（一键呼出）
# 用法: powershell -ExecutionPolicy Bypass -File go_usage_popup.ps1
# 读取 data/go_usage_summary.json，若太旧则尝试实时抓取

$ErrorActionPreference = 'Stop'

$BASE = 'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox'
$JSON = Join-Path $BASE 'data\go_usage_summary.json'

# ---- 数据准备 ----
$data = $null
if (Test-Path $JSON) {
    $age = (Get-Date) - (Get-Item $JSON).LastWriteTime
    if ($age.TotalMinutes -gt 20) {
        # 数据太旧，尝试刷新（失败就用旧数据）
        try {
            Push-Location $BASE
            & python $BASE\cdp_go_page.py 2>$null | Out-Null
            & python $BASE\make_ws_summary.py 2>$null | Out-Null
            Pop-Location
        } catch { Pop-Location }
    }
    $data = Get-Content $JSON -Raw -Encoding UTF8 | ConvertFrom-Json
}

if (-not $data) {
    [System.Windows.Forms.MessageBox]::Show('用量数据获取失败，请检查 Edge CDP 是否在运行', 'Go 用量', 'OK', 'Error') | Out-Null
    exit 1
}

$rolling  = if ($null -ne $data.rolling_pct)  { [int]$data.rolling_pct  } else { 0 }
$weekly   = if ($null -ne $data.weekly_pct)   { [int]$data.weekly_pct   } else { 0 }
$monthly  = if ($null -ne $data.monthly_pct)  { [int]$data.monthly_pct  } else { 0 }
$cost     = if ($null -ne $data.recent_total_cost_usd) { [math]::Round([double]$data.recent_total_cost_usd, 4) } else { 0 }
$sessions = if ($null -ne $data.recent_sessions) { [int]$data.recent_sessions } else { 0 }
$balance  = if ($null -ne $data.balance_usd) { [double]$data.balance_usd } else { $null }
$fetched  = if ($data.fetched_at) { $data.fetched_at } else { '未知' }

function New-Bar([System.Windows.Forms.Control]$parent, [int]$x, [int]$y, [int]$w, [int]$h, [double]$pct) {
    $back = New-Object System.Windows.Forms.Panel
    $back.Location = New-Object System.Drawing.Point($x, $y)
    $back.Size = New-Object System.Drawing.Size($w, $h)
    $back.BackColor = [System.Drawing.Color]::FromArgb(255, 40, 44, 52)
    $parent.Controls.Add($back)

    $fillW = [math]::Max(6, [int]($w * [math]::Min(1.0, $pct / 100.0)))
    $fill = New-Object System.Windows.Forms.Panel
    $fill.Location = New-Object System.Drawing.Point(0, 0)
    $fill.Size = New-Object System.Drawing.Size($fillW, $h)
    if ($pct -ge 80) { $fill.BackColor = [System.Drawing.Color]::FromArgb(255, 231, 76, 60) }
    elseif ($pct -ge 50) { $fill.BackColor = [System.Drawing.Color]::FromArgb(255, 241, 175, 23) }
    else { $fill.BackColor = [System.Drawing.Color]::FromArgb(255, 46, 204, 113) }
    $back.Controls.Add($fill)
    return $back
}

Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$form = New-Object System.Windows.Forms.Form
$form.Text = 'OpenCode Go 用量'
$form.FormBorderStyle = 'None'
$form.BackColor = [System.Drawing.Color]::FromArgb(255, 30, 33, 39)
$form.StartPosition = 'Manual'
$form.TopMost = $true
$form.ShowInTaskbar = $false
$form.Width = 380
$form.Height = 330

# 屏幕上方居中（任务栏上方，留出边距）
$screen = [System.Windows.Forms.Screen]::PrimaryScreen.WorkingArea
$form.Left = $screen.Left + [int](($screen.Width - $form.Width) / 2)
$form.Top = $screen.Top + 12

# 标题
$lblTitle = New-Object System.Windows.Forms.Label
$lblTitle.Text = '📊 OpenCode Go 用量'
$lblTitle.Font = New-Object System.Drawing.Font('Microsoft YaHei UI', 13, [System.Drawing.FontStyle]::Bold)
$lblTitle.ForeColor = [System.Drawing.Color]::White
$lblTitle.Location = New-Object System.Drawing.Point(16, 12)
$lblTitle.Size = New-Object System.Drawing.Size(240, 28)
$form.Controls.Add($lblTitle)

# 关闭按钮
$btnClose = New-Object System.Windows.Forms.Button
$btnClose.Text = '✕'
$btnClose.FlatStyle = 'Flat'
$btnClose.FlatAppearance.BorderSize = 0
$btnClose.BackColor = [System.Drawing.Color]::Transparent
$btnClose.ForeColor = [System.Drawing.Color]::FromArgb(255, 160, 165, 175)
$btnClose.Location = New-Object System.Drawing.Point(340, 8)
$btnClose.Size = New-Object System.Drawing.Size(30, 30)
$btnClose.Add_Click({ $form.Close() })
$form.Controls.Add($btnClose)

# 三行用量进度条
$y = 55
$items = @(
    @{ Label = '🔄 滚动用量'; Val = $rolling;  Sub = $data.rolling_reset },
    @{ Label = '📅 每周用量'; Val = $weekly;   Sub = $data.weekly_reset },
    @{ Label = '📆 每月用量'; Val = $monthly;  Sub = $data.monthly_reset }
)
foreach ($it in $items) {
    $lbl = New-Object System.Windows.Forms.Label
    $lbl.Text = $it.Label + '  ' + $it.Val + '%'
    $lbl.Font = New-Object System.Drawing.Font('Microsoft YaHei UI', 10)
    $lbl.ForeColor = [System.Drawing.Color]::White
    $lbl.Location = New-Object System.Drawing.Point(16, $y)
    $lbl.Size = New-Object System.Drawing.Size(200, 22)
    $form.Controls.Add($lbl)

    $sub = New-Object System.Windows.Forms.Label
    $sub.Text = $it.Sub
    $sub.Font = New-Object System.Drawing.Font('Microsoft YaHei UI', 8)
    $sub.ForeColor = [System.Drawing.Color]::FromArgb(255, 150, 155, 165)
    $sub.Location = New-Object System.Drawing.Point(230, ($y + 2))
    $sub.Size = New-Object System.Drawing.Size(140, 18)
    $sub.TextAlign = 'MiddleRight'
    $form.Controls.Add($sub)

    New-Bar $form 16 ($y + 26) 348 12 ([double]$it.Val) | Out-Null
    $y += 58
}

# 分隔线
$line = New-Object System.Windows.Forms.Label
$line.BackColor = [System.Drawing.Color]::FromArgb(255, 55, 60, 70)
$line.Location = New-Object System.Drawing.Point(16, $y)
$line.Size = New-Object System.Drawing.Size(348, 1)
$form.Controls.Add($line)

$y += 14
# 统计行
$lblStat = New-Object System.Windows.Forms.Label
$balTxt = if ($null -ne $balance) { ('当前余额 $' + $balance) } else { '余额未知' }
$lblStat.Text = "💰 已用 $cost USD · $sessions 次会话 · $balTxt"
$lblStat.Font = New-Object System.Drawing.Font('Microsoft YaHei UI', 9)
$lblStat.ForeColor = [System.Drawing.Color]::White
$lblStat.Location = New-Object System.Drawing.Point(16, $y)
$lblStat.Size = New-Object System.Drawing.Size(348, 24)
$form.Controls.Add($lblStat)
$y += 28

$lblTime = New-Object System.Windows.Forms.Label
$lblTime.Text = "🕐 更新于 $fetched · 点击任意处关闭"
$lblTime.Font = New-Object System.Drawing.Font('Microsoft YaHei UI', 8)
$lblTime.ForeColor = [System.Drawing.Color]::FromArgb(255, 130, 135, 145)
$lblTime.Location = New-Object System.Drawing.Point(16, $y)
$lblTime.Size = New-Object System.Drawing.Size(348, 20)
$form.Controls.Add($lblTime)

# 自动关闭 & 点击关闭
$form.Add_Click({ $form.Close() })
$timer = New-Object System.Windows.Forms.Timer
$timer.Interval = 8000
$timer.Add_Tick({ $form.Close() })
$timer.Start()

$form.ShowDialog() | Out-Null
$timer.Stop()