# coding: utf-8
import argparse
import livechanapi
import config
import commands


def process_chat(api, data):
    if data.get('trip') == config.bot_trip_encoded and data['name'] == config.bot_name:
        return

    for command in commands.commands:
        command(api, data)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("channel", help="name of channel to join")
    args = parser.parse_args()
    api = livechanapi.LiveChanApi(config.url, args.channel, config.password_livechan)
    api.on_chat(process_chat)
    api.wait()


if __name__ == '__main__':
    main()
