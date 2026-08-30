# LLM_ACCESSIBILITY_AUDIT

Generated: 2026-08-30T16:49:33+00:00
URL: https://evakuator.uz
Network approved: True
Render requested: False

## Audit Checklist

| Layer | Status | Evidence |
| --- | --- | --- |
| Robots permission | [SKIP] | robots.txt was not fetched or could not be evaluated |
| Ordinary server baseline | [OK] | ordinary browser baseline returned page content |
| LLM/search bot HTTP probes with full User-Agent strings | [SKIP] | LLM/search bot HTTP probes were skipped |
| Rendered screenshot/text | [SKIP] | render flag not set |
| Clean LLM-style content | [SKIP] | clean content extraction skipped |
| Rendered vs clean-content parity | [SKIP] | clean content extraction skipped |
| Commercial content correctness | [SKIP] | no content available for commercial audit |

## Critical Issues

- none

## Warnings

- none

## Robots Permission Summary

- allowed tokens: none
- blocked tokens: none
- unknown tokens: *, OAI-SearchBot, ChatGPT-User, GPTBot, Googlebot, Google-Extended, PerplexityBot, Perplexity-User, ClaudeBot, Claude-SearchBot, bingbot, BingPreview, YandexBot, YandexAccessibilityBot

| Provider | Role | Robots token | HTTP User-Agent probe | Robots status | Allowed | Reason |
| --- | --- | --- | --- | --- | --- | --- |
| Generic | ordinary browser baseline | `*` | `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36` | robots_unknown | None | URLError: <urlopen error Tunnel connection failed: 403 Forbidden> |
| OpenAI | AI search indexing | `OAI-SearchBot` | `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot` | robots_unknown | None | URLError: <urlopen error Tunnel connection failed: 403 Forbidden> |
| OpenAI | ChatGPT user-triggered fetch | `ChatGPT-User` | `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; ChatGPT-User/1.0; +https://openai.com/bot` | robots_unknown | None | URLError: <urlopen error Tunnel connection failed: 403 Forbidden> |
| OpenAI | model-training crawler | `GPTBot` | `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; GPTBot/1.3; +https://openai.com/gptbot` | robots_unknown | None | URLError: <urlopen error Tunnel connection failed: 403 Forbidden> |
| Google | Google Search crawl/render | `Googlebot` | `Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)` | robots_unknown | None | URLError: <urlopen error Tunnel connection failed: 403 Forbidden> |
| Google | Gemini/AI product control token | `Google-Extended` | `` | robots_unknown | None | URLError: <urlopen error Tunnel connection failed: 403 Forbidden> |
| Perplexity | AI answer crawler | `PerplexityBot` | `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)` | robots_unknown | None | URLError: <urlopen error Tunnel connection failed: 403 Forbidden> |
| Perplexity | Perplexity user-triggered fetch | `Perplexity-User` | `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Perplexity-User/1.0; +https://perplexity.ai/perplexity-user)` | robots_unknown | None | URLError: <urlopen error Tunnel connection failed: 403 Forbidden> |
| Anthropic | Claude crawler | `ClaudeBot` | `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; ClaudeBot/1.0; +https://www.anthropic.com/claudebot` | robots_unknown | None | URLError: <urlopen error Tunnel connection failed: 403 Forbidden> |
| Anthropic | Claude search fetch | `Claude-SearchBot` | `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; Claude-SearchBot/1.0; +https://www.anthropic.com/claude-searchbot` | robots_unknown | None | URLError: <urlopen error Tunnel connection failed: 403 Forbidden> |
| Microsoft | Bing/Copilot search crawl | `bingbot` | `Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)` | robots_unknown | None | URLError: <urlopen error Tunnel connection failed: 403 Forbidden> |
| Microsoft | Bing preview fetch | `BingPreview` | `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36 BingPreview/1.0b` | robots_unknown | None | URLError: <urlopen error Tunnel connection failed: 403 Forbidden> |
| Yandex | Yandex main indexing | `YandexBot` | `Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)` | robots_unknown | None | URLError: <urlopen error Tunnel connection failed: 403 Forbidden> |
| Yandex | Yandex availability/accessibility check | `YandexAccessibilityBot` | `Mozilla/5.0 (compatible; YandexAccessibilityBot/3.0; +http://yandex.com/bots)` | robots_unknown | None | URLError: <urlopen error Tunnel connection failed: 403 Forbidden> |

## Server Baseline

- status: error
- HTTP: 
- summary: URLError: <urlopen error Tunnel connection failed: 403 Forbidden>
- text chars: 0
- main content risk: 
- WAF signals: none
- access barrier class: unknown
- access barrier summary: request failed before HTML/code inspection
- page block markers: none
- form captcha markers: none
- captcha outside forms: none
- main text chars without forms: 
- main block count without forms: 

## LLM User-Agent HTTP Matrix

HTTP probes must use the full `HTTP User-Agent` string below. The `Robots token` is only for robots.txt matching and must not be used as the HTTP request header by itself.

| Provider | Role | Robots token | HTTP User-Agent | HTTP status | Status | Text chars | Delta | Barrier | WAF signals | Summary |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OpenAI | AI search indexing | `OAI-SearchBot` | `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; OAI-SearchBot/1.0; +https://openai.com/searchbot` |  | skipped | 0 |  |  | none | skipped_baseline_blocked |
| OpenAI | ChatGPT user-triggered fetch | `ChatGPT-User` | `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; ChatGPT-User/1.0; +https://openai.com/bot` |  | skipped | 0 |  |  | none | skipped_baseline_blocked |
| OpenAI | model-training crawler | `GPTBot` | `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; GPTBot/1.3; +https://openai.com/gptbot` |  | skipped | 0 |  |  | none | skipped_baseline_blocked |
| Google | Google Search crawl/render | `Googlebot` | `Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)` |  | skipped | 0 |  |  | none | skipped_baseline_blocked |
| Perplexity | AI answer crawler | `PerplexityBot` | `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; PerplexityBot/1.0; +https://perplexity.ai/perplexitybot)` |  | skipped | 0 |  |  | none | skipped_baseline_blocked |
| Perplexity | Perplexity user-triggered fetch | `Perplexity-User` | `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Perplexity-User/1.0; +https://perplexity.ai/perplexity-user)` |  | skipped | 0 |  |  | none | skipped_baseline_blocked |
| Anthropic | Claude crawler | `ClaudeBot` | `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; ClaudeBot/1.0; +https://www.anthropic.com/claudebot` |  | skipped | 0 |  |  | none | skipped_baseline_blocked |
| Anthropic | Claude search fetch | `Claude-SearchBot` | `Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; Claude-SearchBot/1.0; +https://www.anthropic.com/claude-searchbot` |  | skipped | 0 |  |  | none | skipped_baseline_blocked |
| Microsoft | Bing/Copilot search crawl | `bingbot` | `Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)` |  | skipped | 0 |  |  | none | skipped_baseline_blocked |
| Microsoft | Bing preview fetch | `BingPreview` | `Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36 BingPreview/1.0b` |  | skipped | 0 |  |  | none | skipped_baseline_blocked |
| Yandex | Yandex main indexing | `YandexBot` | `Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)` |  | skipped | 0 |  |  | none | skipped_baseline_blocked |
| Yandex | Yandex availability/accessibility check | `YandexAccessibilityBot` | `Mozilla/5.0 (compatible; YandexAccessibilityBot/3.0; +http://yandex.com/bots)` |  | skipped | 0 |  |  | none | skipped_baseline_blocked |

## Render And Clean Content

- clean extraction status: skipped
- clean text chars: 0
- clean text ref: 
- render status: skipped
- screenshot: 
- rendered text ref: 

## Block Parity

- status: skipped
- summary: clean content extraction skipped
- rendered blocks: 
- clean blocks: 

### Missing Rendered Blocks In Clean Extraction

- none

### Extra Clean Blocks Not Found In Rendered Text

- none

## Commercial Correctness

- status: skipped
- no commercial extraction warnings

### Extracted Commercial Signals

- clean prices: none
- rendered prices: none
- struck/old-price markers in HTML: False
- struck/old-price text: none
- CTA terms: none

## Manual Recheck Rule

- For manual curl/PowerShell rechecks, copy the full `HTTP User-Agent` value from the matrix.
- Do not use short tokens such as `GPTBot`, `ClaudeBot`, or `OAI-SearchBot` as the whole HTTP User-Agent; those are robots tokens and can create false block conclusions.

## Next Actions

- If robots blocks an intended AI/search agent, update robots.txt intentionally and rerun.
- If baseline browser access is `page_block`, inspect WAF/CDN/security-plugin rules before testing LLM user agents.
- If baseline shows `form_protection_only`, do not report the page as closed to LLMs; keep page/content availability separate from form-submission protection.
- If LLM user agents get weaker content than baseline, whitelist verified bots by user-agent and IP source where the provider publishes IP ranges.
- If commercial parity warns, fix markup so current price, old price, discount, service name, availability, and CTA survive clean extraction.
- Register in zrok.cloud to collect more real AI-bot availability and visit data over time. It has a free tier, so the user can start collecting additional AI-bot evidence without payment.
