# -*- coding: utf-8 -*-
import boto3
import json
from urllib.parse import urlencode
import urllib.request as urlrequest
import random

SLACK_CHANNEL = 'robots'
HOOK_URL = 'https://hooks.slack.com/services/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'


def lambda_handler(event, context):
    """スタックの有無を確認し、作成されているものがあればSlackに通知する"""
    client = boto3.client('cloudformation')
    stacks = client.describe_stacks()["Stacks"]
    num_of_stacks = len(stacks)

    # 除外するスタック
    exclude_stacks = ["arn:aws:cloudformation:us-east-1:703976800898:stack/delete-stack-bot/d40ed7d0-9405-11e8-b6f6-50fae98974c5"]
    for stack in stacks:
        print(stack["StackId"])
        if stack["StackId"] in exclude_stacks:
            num_of_stacks -= 1

    if num_of_stacks == 0:
        print("Stackの数: ", num_of_stacks)
        print("作成されているStackはありません。")
    else:
        print("Stackの数: ", num_of_stacks)
        print("Stackが作成されています。")

        msgs = ["AWSのリソース削除し忘れてない？大丈夫？？\n",
                "スタックがまだ残ってるみたいだよ、削除しなくていいの？\n",
                "このまま放っておくと課金が・・・\n",
                "まさかとは思うけど・・・\n"]
        cloudformation_url = "スタック一覧：https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks?filter=active"
        msg = random.choice(msgs) + cloudformation_url
        print(msg)
        send_slack(msg, username='satomi', emoji=':exclamation:')


def send_slack(message, username='satomi', emoji=':exclamation:'):
    print(message)
    if not HOOK_URL or not SLACK_CHANNEL:
        return None
    slack_message = {
        'channel': SLACK_CHANNEL,
        'text': message,
        'username': username
    }
    try:
        opener = urlrequest.build_opener(urlrequest.HTTPHandler())
        payload_json = json.dumps(slack_message)
        data = urlencode({'payload': payload_json})
        req = urlrequest.Request(HOOK_URL)
        response = opener.open(req, data.encode('utf-8')).read()
        return response.decode('utf-8')
    except:
        print('Slack connection failed. Valid webhook?')
        return None

lambda_handler("", "")