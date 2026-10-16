#!/usr/bin/env python3
"""Tiny TypeSafe Jev helper for Toolome judgment calls.
Reads the API key from $TYPESAFE_API_KEY or /home/box/.typesafe_key (never printed).
  from jev import ask, choice, noul, score
  r = ask(state, {'cat': choice('Which category', {'a': 'desc', ...}), 'x': noul('Statement')})
  r['answers']['cat']['choice'], r['answers']['x']['noul'], r['usage']
"""
import json, os, urllib.request, time
PRICE_IN, PRICE_OUT = 0.042, 0.0  # $ per 1M tokens (TypeSafe docs, jev-1.12+)
SPENT = {'in': 0, 'out': 0}
def _key():
    k = os.environ.get('TYPESAFE_API_KEY')
    return k or open('/home/box/.typesafe_key').read().strip()
def choice(instructions, criteria): return {'type': 'choice', 'instructions': instructions, 'criteria': criteria}
def noul(instructions): return {'type': 'noul', 'instructions': instructions}
def score(instructions, criteria): return {'type': 'score', 'instructions': instructions, 'criteria': criteria}
def ask(state, questions, model='jev-latest', retries=3):
    body = json.dumps({'model': model, 'state': state, 'questions': questions}).encode()
    for i in range(retries):
        try:
            req = urllib.request.Request('https://api.typesafe.ai/v1/systemone', data=body,
                  headers={'Authorization': 'Bearer ' + _key(), 'Content-Type': 'application/json'})
            r = json.load(urllib.request.urlopen(req, timeout=90))
            SPENT['in'] += r['usage']['input_tokens']; SPENT['out'] += r['usage']['output_tokens']
            return r
        except Exception:
            if i == retries - 1: raise
            time.sleep(2 * (i + 1))
def cost(): return SPENT['in'] / 1e6 * PRICE_IN + SPENT['out'] / 1e6 * PRICE_OUT
