# -*- coding: utf-8 -*-
"""生成 iPhone 快捷指令安装包 (.shortcut)
动作: 获取URL内容(go_usage.txt) → 显示通知(屏幕上方横幅)
输出: atm-toolbox/downloads/Go用量.shortcut
"""
import plistlib, os, struct

BASE = r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox'
OUT_DIR = os.path.join(BASE, 'downloads')
os.makedirs(OUT_DIR, exist_ok=True)
OUT = os.path.join(OUT_DIR, 'Go用量.shortcut')

workflow = {
    'WFWorkflowClientVersion': '900',
    'WFWorkflowClientRelease': '2.1',
    'WFWorkflowImportQuestions': [],
    'WFWorkflowHasShortcutInputVariables': 0,
    'WFWorkflowMinimumClientVersion': 900,
    'WFWorkflowMinimumClientVersionString': '900',
    'WFWorkflowInputContentItemClasses': [
        'WFAppStoreAppContentItem', 'WFArticleContentItem', 'WFContactContentItem',
        'WFDateContentItem', 'WFEmailAddressContentItem', 'WFGenericFileContentItem',
        'WFImageContentItem', 'WFiTunesProductContentItem', 'WFLocationContentItem',
        'WFDCMapsLinkContentItem', 'WFAVAssetContentItem', 'WFPDFContentItem',
        'WFPhoneNumberContentItem', 'WFRichTextContentItem', 'WFSafariWebPageContentItem',
        'WFStringContentItem', 'WFURLContentItem',
    ],
    'WFWorkflowTypes': ['NCWidget', 'WatchKit'],
    'WFWorkflowIcon': {
        'WFWorkflowIconGlyphNumber': 59777,  # 📊 (0xE981)
        'WFWorkflowIconStartColor': 4282601983,
    },
    'WFWorkflowName': 'Go 用量',
    'WFWorkflowActions': [
        {
            # 动作1: 获取 URL 内容
            'WFWorkflowActionIdentifier': 'is.workflow.actions.downloadurl',
            'WFWorkflowActionParameters': {
                'WFURL': 'https://atemmie.github.io/atm-toolbox/data/go_usage.txt',
                'WFHTTPMethod': 'GET',
            },
        },
        {
            # 动作2: 显示通知（顶部横幅弹窗）
            'WFWorkflowActionIdentifier': 'is.workflow.actions.notification',
            'WFWorkflowActionParameters': {
                'WFNotificationActionTitle': '📊 OpenCode Go 用量',
                # body 留空 = 使用上一个动作的输出文本
            },
        },
    ],
}

with open(OUT, 'wb') as f:
    plistlib.dump(workflow, f, fmt=plistlib.FMT_BINARY, sort_keys=False)

size = os.path.getsize(OUT)
head = open(OUT, 'rb').read(8)
print(f'✅ 已生成: {OUT} ({size} bytes)')
print(f'   头部: {head.hex()} (bplist00 = 有效二进制plist)')

# 验证可读回
with open(OUT, 'rb') as f:
    back = plistlib.load(f)
print(f'   回读验证: name={back["WFWorkflowName"]}, actions={len(back["WFWorkflowActions"])}')