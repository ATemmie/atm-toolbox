# -*- coding: utf-8 -*-
"""生成《和Hermes语音对话》快捷指令安装包 v2
动作链:
  1. 听写文本(跟随系统语言)
  2. URL 编码听写文本 → 变量 enc
  3. 获取 URL 内容(发送): https://webhook.site/<uuid>?t=<enc>
  4. 显示通知「已发送」
  5. 等待 10s
  6. 获取 URL 内容: 读取回复文件 (raw)
  7. 显示通知: 回复内容（自动接上一步输出）
注意: 魔法变量用标准 WFTextTokenString 格式（string='%%', range {0,2}）
"""
import plistlib, os, uuid as uuidlib

BASE = r'C:\Users\Administrator\Desktop\传输\projects\atm-toolbox'
OUT = os.path.join(BASE, 'downloads', 'voice-chat.shortcut')
HOOK_UUID = '1ff82e20-da23-47b0-890e-27850f6c1b11'
TXT_URL = 'https://raw.githubusercontent.com/ATemmie/atm-toolbox/main/data/voice_reply.txt'

def wf_text_var(out_uuid, out_name):
    """标准魔法变量：string=%% 占位, attachmentsByRange {0,2}"""
    return {
        'WFSerializationType': 'WFTextTokenString',
        'Value': {
            'attachmentsByRange': {
                '{0, 2}': {'OutputUUID': out_uuid, 'OutputName': out_name},
            },
            'string': '%%',
        },
    }

def act(identifier, params=None, out_name=None):
    a = {'WFWorkflowActionIdentifier': identifier,
         'WFWorkflowActionParameters': params or {}}
    if out_name:
        a['WFWorkflowActionParameters']['WFOutputUUID'] = uuidlib.uuid4().hex.upper()
        a['WFWorkflowActionParameters']['WFOutputName'] = out_name
    return a

uuid_text = uuidlib.uuid4().hex.upper()
uuid_enc = uuidlib.uuid4().hex.upper()

actions = [
    # 1. 听写文本
    act('is.workflow.actions.dictatetext', {}, out_name='text'),
    # 2. URL 编码（自动接上一个动作输出）
    act('is.workflow.actions.urlencode', {}, out_name='enc'),
    # 3. 发送
    act('is.workflow.actions.downloadurl', {
        'WFHTTPMethod': 'GET',
        'WFURL': 'https://webhook.site/' + HOOK_UUID + '?t=%%',
        'WFURLMagic': wf_text_var(uuid_enc, 'enc'),
    }),
    # 4. 已发送通知
    act('is.workflow.actions.notification', {
        'WFNotificationActionTitle': '📨 已发给 Hermes',
        'WFNotificationActionBody': '等待回复中（约 30-60 秒）…',
    }),
    # 5. 等待 10s
    act('is.workflow.actions.delay', {'WFDelayTime': 10}),
    # 6. 读取回复
    act('is.workflow.actions.downloadurl', {
        'WFHTTPMethod': 'GET',
        'WFURL': TXT_URL,
    }),
    # 7. 显示回复
    act('is.workflow.actions.notification', {
        'WFNotificationActionTitle': '🤖 Hermes 回复',
    }),
]

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
        'WFWorkflowIconGlyphNumber': 59732,
        'WFWorkflowIconStartColor': 4287917378,
    },
    'WFWorkflowName': '和Hermes语音对话',
    'WFWorkflowActions': actions,
}

with open(OUT, 'wb') as f:
    plistlib.dump(workflow, f, fmt=plistlib.FMT_BINARY, sort_keys=False)

print(f'✅ {os.path.basename(OUT)} 已生成 ({os.path.getsize(OUT)} bytes)')
with open(OUT, 'rb') as f:
    back = plistlib.load(f)
print(f'   回读: name={back["WFWorkflowName"]}, actions={len(back["WFWorkflowActions"])}')
for i, a in enumerate(back['WFWorkflowActions']):
    print(f"   {i+1}. {a['WFWorkflowActionIdentifier']}")