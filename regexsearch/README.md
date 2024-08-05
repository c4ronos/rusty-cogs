### ~~Supports slash commands~~
<h1></h1>

# INFO
---
➥ Limited by discord search? Use this cog to search messages with regex.
<br/><br/>
➥ Only admins can enter a limit greater than 5000.
<br/><br/>
➥ It is suggested to use the inbuilt permissions cog to prevent misuse of this cog.

# USAGE
---
➥ `[p]regex <pattern> [flags]`
<br/><br/>
➥ `[p]regex help` for the list of flags and some examples

# FLAGS
---
- `--limit <int>` - The amount of messages to process. default:`500`, min:`1`, max:`10.000`
<br/><br/>
- `--channel <channel>` - Search messages in a specific channel. Value can be id/mention.
<br/><br/>
- `--user <user>` - Search messages only from this user. Value can be username/id/mention.
<br/><br/>
- `--not-user <user>` - Do not search messages from this user. Value can be username/id/mention
<br/><br/>
- `--bots` - Search messages also from bots.
<br/><br/>
- `--only-bots` - Search messages only from bots.
<br/><br/>
- `--media` - Include messages with attachments in the search results.
<br/><br/>
- `--only-media` - Only search messages with attachments.
<br/><br/>
- `--embeds` - Include messages with embeds in the search results.
<br/><br/>
- `--only-embeds` - Only search messages with embeds.

# RESOURCES
---
➥ Recommended for trying regex: https://regex101.com/
<br/><br/>
➥ Basic regex cheatsheat: [simple_regex.md](.archive/simple_regex.md)

# EXAMPLES
---
- `[p]regex .* --limit 1000 --channel #general --user @egirl`\
will return all messages sent by @egirl in #general's last 1000 messages.
<br/><br/>
- `[p]regex (discord\.gg/)[A-Za-z0-9]?.* --channel #general`\
will return all server invite links in #general's last 500 messages.
<br/><br/>
- `[p]regex (?i)(help|helpp|helppp) --limit 5000`\
will return all instances of help, helpp, helppp found in current channel's last 5000 messages. (?i) makes it case-insensitive.
