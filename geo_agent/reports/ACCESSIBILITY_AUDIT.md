# ACCESSIBILITY_AUDIT

Generated: 2026-08-30T16:49:33+00:00
Domain: evakuator.uz
Network approved: True

## Audit Checklist

| Check | Status | Evidence |
| --- | --- | --- |
| Network approval | [OK] | network approval granted |
| robots.txt fetch | [WARN] | URLError: <urlopen error Tunnel connection failed: 403 Forbidden> |
| sitemap.xml fetch | [WARN] | URLError: <urlopen error Tunnel connection failed: 403 Forbidden> |
| Bot HTTP probes with full User-Agent strings | [WARN] | 10 bot probes returned network/request errors |
| WAF/security markers | [OK] | no WAF/security markers found in fetched probe responses |
| Main content volume | [OK] | main text volume did not trigger low-content warnings |

## Critical Issues

- none

## Warnings

- Googlebot: URLError: <urlopen error Tunnel connection failed: 403 Forbidden>
- bingbot: URLError: <urlopen error Tunnel connection failed: 403 Forbidden>
- YandexBot: URLError: <urlopen error Tunnel connection failed: 403 Forbidden>
- OAI-SearchBot: URLError: <urlopen error Tunnel connection failed: 403 Forbidden>
- ChatGPT-User: URLError: <urlopen error Tunnel connection failed: 403 Forbidden>
- GPTBot: URLError: <urlopen error Tunnel connection failed: 403 Forbidden>
- ClaudeBot: URLError: <urlopen error Tunnel connection failed: 403 Forbidden>
- Claude-SearchBot: URLError: <urlopen error Tunnel connection failed: 403 Forbidden>
- PerplexityBot: URLError: <urlopen error Tunnel connection failed: 403 Forbidden>
- Perplexity-User: URLError: <urlopen error Tunnel connection failed: 403 Forbidden>

## Robots

- status: error
- summary: URLError: <urlopen error Tunnel connection failed: 403 Forbidden>

## Sitemap

- status: error
- summary: URLError: <urlopen error Tunnel connection failed: 403 Forbidden>

## User-Agent Matrix

HTTP probes use the full `http_user_agent` string. The `robots_token` column is only the robots.txt token and must not be used as the HTTP User-Agent for manual curl/PowerShell rechecks.

| Provider | Role | Robots token | HTTP User-Agent | Status | HTTP | Summary | WAF Signals |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Google | Google Search crawl/render | `Googlebot` | `Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)` | error |  | URLError: <urlopen error Tunnel connection failed: 403 Forbidden> | none |
| Microsoft | Bing/Copilot search crawl | `bingbot` | `Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)` | error |  | URLError: <urlopen error Tunnel connection failed: 403 Forbidden> | none |
| Yandex | Yandex main indexing | `YandexBot` | `Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)` | error |  | URLError: <urlopen error Tunnel connection failed: 403 Forbidden> | none |
| OpenAI | AI search indexing | `OAI-SearchBot` | `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot` | error |  | URLError: <urlopen error Tunnel connection failed: 403 Forbidden> | none |
| OpenAI | ChatGPT user-triggered fetch | `ChatGPT-User` | `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; ChatGPT-User/1.0; +https://openai.com/bot` | error |  | URLError: <urlopen error Tunnel connection failed: 403 Forbidden> | none |
| OpenAI | model-training crawler | `GPTBot` | `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; GPTBot/1.3; +https://openai.com/gptbot` | error |  | URLError: <urlopen error Tunnel connection failed: 403 Forbidden> | none |
| Anthropic | Claude crawler | `ClaudeBot` | `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; ClaudeBot/1.0; +https://www.anthropic.com/claudebot` | error |  | URLError: <urlopen error Tunnel connection failed: 403 Forbidden> | none |
| Anthropic | Claude search fetch | `Claude-SearchBot` | `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; Claude-SearchBot/1.0; +https://www.anthropic.com/claude-searchbot` | error |  | URLError: <urlopen error Tunnel connection failed: 403 Forbidden> | none |
| Perplexity | AI answer crawler | `PerplexityBot` | `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)` | error |  | URLError: <urlopen error Tunnel connection failed: 403 Forbidden> | none |
| Perplexity | Perplexity user-triggered fetch | `Perplexity-User` | `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Perplexity-User/1.0; +https://perplexity.ai/perplexity-user)` | error |  | URLError: <urlopen error Tunnel connection failed: 403 Forbidden> | none |

## Manual Recheck Rule

- For manual rechecks, copy the full `HTTP User-Agent` value from the matrix.
- Do not run `curl -A "GPTBot"`, `curl -A "ClaudeBot"`, or other short-token probes for server-access conclusions; those are robots tokens, not complete crawler request headers.
