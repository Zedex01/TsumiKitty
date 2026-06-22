
import os
import time
import re
import logging
import asyncio

from pathlib import Path

from src.util.Config import Config

class LogWatcher:

    JOIN_PATTERN = re.compile(r": (.+?) joined the game")
    LEAVE_PATTERN = re.compile(r": (.+?) left the game")
    ADVANCEMENT_PATTERN = re.compile(r": (.+?) has made the advancement \[(.+?)\]")

    def __init__(self, bot):
        self.cfg = Config() #create config

        self.log_path = Path(self.cfg.get_str("Setup","server_dir")) / "logs" / "latest.log"
        print(self.log_path)

        self.bot = bot
        
        self._file = None
        self._running = False

    def start(self):
        """Open the log file and seek to the end (like tail -f)."""
        #print("Starting log watcher")
        self._file = open(self.log_path, "r", encoding="utf-8")
        self._file.seek(0, os.SEEK_END)
        self._running = True
        #print("Found end of log file")

    def stop(self):
        if self._file:
            self._file.close()
        self._running = False
            
    async def watch(self):
        """Cont read from log"""
        self.start()
        while self._running:
            line = self._file.readline()
            if not line:
                await asyncio.sleep(0.1)
                continue
                
            #join
            m = self.JOIN_PATTERN.search(line)
            if m:
                await self.on_event({"event": "join", "player":m.group(1)})
                continue
            #leave
            
            m = self.LEAVE_PATTERN.search(line)
            if m:
                await self.on_event({"event": "leave", "player":m.group(1)})
                continue
    
            m = self.ADVANCEMENT_PATTERN.search(line)
            if m:
                await self.on_event({"event": "advancement", "player":m.group(1), "advancement":m.group(2)})
                continue
                
    async def on_event(self, event: dict):
        """Hook for handling events, override or replace this in your bot"""
        #print(f"[LOG WATCHER] {event}")
        channel_id = self.cfg.get_int("Notices", "channel_id")
        channel = self.bot.get_channel(channel_id)
        if channel:
            if event["event"] == "join":
                await channel.send(f"✅ **{event['player']}** joined the game")
            elif event["event"] == "leave":
                await channel.send(f"❌ **{event['player']}** left the game")
            elif event["event"] == "advancement":
                await channel.send(
                    f"🏆 **{event['player']}** made advancement: {event['advancement']}"
                )