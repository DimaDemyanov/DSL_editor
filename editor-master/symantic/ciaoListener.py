# Generated from ciao.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .ciaoParser import ciaoParser
else:
    from ciaoParser import ciaoParser

# This class defines a complete listener for a parse tree1 produced by ciaoParser.
class ciaoListener(ParseTreeListener):

    # Enter a parse tree1 produced by ciaoParser#p.
    def enterP(self, ctx:ciaoParser.PContext):
        pass

    # Exit a parse tree1 produced by ciaoParser#p.
    def exitP(self, ctx:ciaoParser.PContext):
        pass


    # Enter a parse tree1 produced by ciaoParser#n.
    def enterN(self, ctx:ciaoParser.NContext):
        pass

    # Exit a parse tree1 produced by ciaoParser#n.
    def exitN(self, ctx:ciaoParser.NContext):
        pass


    # Enter a parse tree1 produced by ciaoParser#v.
    def enterV(self, ctx:ciaoParser.VContext):
        pass

    # Exit a parse tree1 produced by ciaoParser#v.
    def exitV(self, ctx:ciaoParser.VContext):
        pass


    # Enter a parse tree1 produced by ciaoParser#e.
    def enterE(self, ctx:ciaoParser.EContext):
        pass

    # Exit a parse tree1 produced by ciaoParser#e.
    def exitE(self, ctx:ciaoParser.EContext):
        pass


    # Enter a parse tree1 produced by ciaoParser#a.
    def enterA(self, ctx:ciaoParser.AContext):
        pass

    # Exit a parse tree1 produced by ciaoParser#a.
    def exitA(self, ctx:ciaoParser.AContext):
        pass


    # Enter a parse tree1 produced by ciaoParser#r.
    def enterR(self, ctx:ciaoParser.RContext):
        pass

    # Exit a parse tree1 produced by ciaoParser#r.
    def exitR(self, ctx:ciaoParser.RContext):
        pass


    # Enter a parse tree1 produced by ciaoParser#q.
    def enterQ(self, ctx:ciaoParser.QContext):
        pass

    # Exit a parse tree1 produced by ciaoParser#q.
    def exitQ(self, ctx:ciaoParser.QContext):
        pass


    # Enter a parse tree1 produced by ciaoParser#u.
    def enterU(self, ctx:ciaoParser.UContext):
        pass

    # Exit a parse tree1 produced by ciaoParser#u.
    def exitU(self, ctx:ciaoParser.UContext):
        pass


    # Enter a parse tree1 produced by ciaoParser#funcCondition.
    def enterFuncCondition(self, ctx:ciaoParser.FuncConditionContext):
        pass

    # Exit a parse tree1 produced by ciaoParser#funcCondition.
    def exitFuncCondition(self, ctx:ciaoParser.FuncConditionContext):
        pass


    # Enter a parse tree1 produced by ciaoParser#exprCondition.
    def enterExprCondition(self, ctx:ciaoParser.ExprConditionContext):
        pass

    # Exit a parse tree1 produced by ciaoParser#exprCondition.
    def exitExprCondition(self, ctx:ciaoParser.ExprConditionContext):
        pass


    # Enter a parse tree1 produced by ciaoParser#exprAction.
    def enterExprAction(self, ctx:ciaoParser.ExprActionContext):
        pass

    # Exit a parse tree1 produced by ciaoParser#exprAction.
    def exitExprAction(self, ctx:ciaoParser.ExprActionContext):
        pass


    # Enter a parse tree1 produced by ciaoParser#funcAction.
    def enterFuncAction(self, ctx:ciaoParser.FuncActionContext):
        pass

    # Exit a parse tree1 produced by ciaoParser#funcAction.
    def exitFuncAction(self, ctx:ciaoParser.FuncActionContext):
        pass


    # Enter a parse tree1 produced by ciaoParser#variables.
    def enterVariables(self, ctx:ciaoParser.VariablesContext):
        pass

    # Exit a parse tree1 produced by ciaoParser#variables.
    def exitVariables(self, ctx:ciaoParser.VariablesContext):
        pass


    # Enter a parse tree1 produced by ciaoParser#values.
    def enterValues(self, ctx:ciaoParser.ValuesContext):
        pass

    # Exit a parse tree1 produced by ciaoParser#values.
    def exitValues(self, ctx:ciaoParser.ValuesContext):
        pass


    # Enter a parse tree1 produced by ciaoParser#notExpr.
    def enterNotExpr(self, ctx:ciaoParser.NotExprContext):
        pass

    # Exit a parse tree1 produced by ciaoParser#notExpr.
    def exitNotExpr(self, ctx:ciaoParser.NotExprContext):
        pass


    # Enter a parse tree1 produced by ciaoParser#unaryMinusExpr.
    def enterUnaryMinusExpr(self, ctx:ciaoParser.UnaryMinusExprContext):
        pass

    # Exit a parse tree1 produced by ciaoParser#unaryMinusExpr.
    def exitUnaryMinusExpr(self, ctx:ciaoParser.UnaryMinusExprContext):
        pass


    # Enter a parse tree1 produced by ciaoParser#func.
    def enterFunc(self, ctx:ciaoParser.FuncContext):
        pass

    # Exit a parse tree1 produced by ciaoParser#func.
    def exitFunc(self, ctx:ciaoParser.FuncContext):
        pass


    # Enter a parse tree1 produced by ciaoParser#multiplicationExpr.
    def enterMultiplicationExpr(self, ctx:ciaoParser.MultiplicationExprContext):
        pass

    # Exit a parse tree1 produced by ciaoParser#multiplicationExpr.
    def exitMultiplicationExpr(self, ctx:ciaoParser.MultiplicationExprContext):
        pass


    # Enter a parse tree1 produced by ciaoParser#atomExpr.
    def enterAtomExpr(self, ctx:ciaoParser.AtomExprContext):
        pass

    # Exit a parse tree1 produced by ciaoParser#atomExpr.
    def exitAtomExpr(self, ctx:ciaoParser.AtomExprContext):
        pass


    # Enter a parse tree1 produced by ciaoParser#orExpr.
    def enterOrExpr(self, ctx:ciaoParser.OrExprContext):
        pass

    # Exit a parse tree1 produced by ciaoParser#orExpr.
    def exitOrExpr(self, ctx:ciaoParser.OrExprContext):
        pass


    # Enter a parse tree1 produced by ciaoParser#additiveExpr.
    def enterAdditiveExpr(self, ctx:ciaoParser.AdditiveExprContext):
        pass

    # Exit a parse tree1 produced by ciaoParser#additiveExpr.
    def exitAdditiveExpr(self, ctx:ciaoParser.AdditiveExprContext):
        pass


    # Enter a parse tree1 produced by ciaoParser#relationalExpr.
    def enterRelationalExpr(self, ctx:ciaoParser.RelationalExprContext):
        pass

    # Exit a parse tree1 produced by ciaoParser#relationalExpr.
    def exitRelationalExpr(self, ctx:ciaoParser.RelationalExprContext):
        pass


    # Enter a parse tree1 produced by ciaoParser#equalityExpr.
    def enterEqualityExpr(self, ctx:ciaoParser.EqualityExprContext):
        pass

    # Exit a parse tree1 produced by ciaoParser#equalityExpr.
    def exitEqualityExpr(self, ctx:ciaoParser.EqualityExprContext):
        pass


    # Enter a parse tree1 produced by ciaoParser#andExpr.
    def enterAndExpr(self, ctx:ciaoParser.AndExprContext):
        pass

    # Exit a parse tree1 produced by ciaoParser#andExpr.
    def exitAndExpr(self, ctx:ciaoParser.AndExprContext):
        pass


    # Enter a parse tree1 produced by ciaoParser#parExpr.
    def enterParExpr(self, ctx:ciaoParser.ParExprContext):
        pass

    # Exit a parse tree1 produced by ciaoParser#parExpr.
    def exitParExpr(self, ctx:ciaoParser.ParExprContext):
        pass


    # Enter a parse tree1 produced by ciaoParser#numberAtom.
    def enterNumberAtom(self, ctx:ciaoParser.NumberAtomContext):
        pass

    # Exit a parse tree1 produced by ciaoParser#numberAtom.
    def exitNumberAtom(self, ctx:ciaoParser.NumberAtomContext):
        pass


    # Enter a parse tree1 produced by ciaoParser#booleanAtom.
    def enterBooleanAtom(self, ctx:ciaoParser.BooleanAtomContext):
        pass

    # Exit a parse tree1 produced by ciaoParser#booleanAtom.
    def exitBooleanAtom(self, ctx:ciaoParser.BooleanAtomContext):
        pass


    # Enter a parse tree1 produced by ciaoParser#idAtom.
    def enterIdAtom(self, ctx:ciaoParser.IdAtomContext):
        pass

    # Exit a parse tree1 produced by ciaoParser#idAtom.
    def exitIdAtom(self, ctx:ciaoParser.IdAtomContext):
        pass


    # Enter a parse tree1 produced by ciaoParser#stringAtom.
    def enterStringAtom(self, ctx:ciaoParser.StringAtomContext):
        pass

    # Exit a parse tree1 produced by ciaoParser#stringAtom.
    def exitStringAtom(self, ctx:ciaoParser.StringAtomContext):
        pass


