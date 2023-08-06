# -*- coding: utf-8 -*-
# This file is part of Quark-Engine - https://github.com/quark-engine/quark-engine
# See the file 'LICENSE' for copying permission.

import functools
from os import PathLike

from quark.core.analysis import QuarkAnalysis
from quark.core.quark import Quark
from quark.core.struct.ruleobject import RuleObject


@functools.cache
def _get_quark(apk: PathLike) -> Quark:
    return Quark(apk)


@functools.cache
def _get_rule_obj(rule: PathLike) -> RuleObject:
    return RuleObject(rule)


@functools.cache
def _run_analysis_on_rule(apk: PathLike, rule: PathLike) -> QuarkAnalysis:
    quark = _get_quark(apk)
    rule_obj = _get_rule_obj(rule)

    quark.run(rule_obj)

    # * 將 quark.quark_analysis 替換成新的 analysi
    analysis = quark.quark_analysis
    quark.quark_analysis = QuarkAnalysis()
    return analysis


def is_behavior_found(apk: PathLike, rule: PathLike) -> bool:
    analysis = _run_analysis_on_rule(apk, rule)
    return bool(analysis.level_5_result)


def has_string_in_behavior(
    apk: PathLike, rule: PathLike, pattern: str
) -> bool:
    analysis = _run_analysis_on_rule(apk, rule)
    quark = _get_quark(apk)

    # * 將 quark.quark_analysis 替換成新的 analysi
    analysis_result = QuarkAnalysis()
    analysis_backup = quark.quark_analysis

    quark.quark_analysis = analysis_result

    for call_graph_analysis in analysis.call_graph_analysis_list:
        arg_mapping_dict = {
            "parent_function": call_graph_analysis["parent"],
            "first_method_list": (call_graph_analysis["first_call"],),
            "second_method_list": (call_graph_analysis["second_call"],),
            "keyword_item_list": ((pattern,), (pattern,)),
        }

        quark.check_parameter(**arg_mapping_dict)

    # * 將 quark.quark_analysis 復原
    quark.quark_analysis = analysis_backup
    return bool(analysis_result.parent_wrapper_mapping)
