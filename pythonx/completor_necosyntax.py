# -*- coding: utf-8 -*-

import logging
from completor import Completor, vim

_cache = {}

logger = logging.getLogger('completor')


class Necosyntax(Completor):
    filetype = 'necosyntax'
    sync = True

    def __init__(self):
        super(Completor, self).__init__()
        necosyntax_init = vim.Function('necosyntax#initialize')
        necosyntax_init()

    def _get_candidates(self):
        get_candidates = vim.Function('necosyntax#gather_candidates')
        candidates = [{
            'word': word,
            'dup': 1,
            'menu': b'[S]'
        } for word in get_candidates()[:]]
        candidates.sort(key=lambda x: x['word'])
        return candidates

    def parse(self, base):
        if not self.ft or not base or base.endswith((' ', '\t')):
            return []

        if self.ft not in _cache:
            try:
                _cache[self.ft] = self._get_candidates()
            except Exception:
                _cache[self.ft] = []

        token = self.input_data.split()[-1]
        candidates = [dict(item) for item in _cache[self.ft]
                      if item['word'].startswith(token.encode('utf-8'))]
        logger.info(candidates)

        offset = len(self.input_data) - len(token)
        for c in candidates:
            c['abbr'] = c['word']
            c['offset'] = offset
        return candidates
