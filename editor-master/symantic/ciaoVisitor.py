# Generated from ciao.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .ciaoParser import ciaoParser
else:
    from ciaoParser import ciaoParser
import json

# This class defines a complete generic visitor for a parse tree1 produced by ciaoParser.

class ciaoVisitor(ParseTreeVisitor):

    def __init__(self):
        ParseTreeVisitor.__init__(self)
        # self.graphs[self.k] = {}
        # self.graphs[self.k]['name'] = ""
        # self.graphs[self.k]['var'] = []
        # self.graphs[self.k]['required'] = []
        # self.graphs[self.k]['provided'] = []
        # self.graphs[self.k]['inner'] = []
        # self.graphs[self.k]['query'] = []
        # self.graphs[self.k]['state'] = []
        self.graphs = []
        self.k = -1


    def print_dict(self, symanticName, dir):
        # print(json.dumps(self.graphs[self.k], indent=2))
        f = open(dir + '/' + symanticName + '/' + symanticName + '.dot', "w")
        print("digraph {", sep='', file=f)
        print("compound=true;", sep='', file=f)
        ind = -1
        for program in self.graphs:
            ind += 1
            print("subgraph cluster{i}".format(i=ind) + ' {', sep='', file=f)

            table = """
            <<table border="0" cellspacing="0" cellborder="1">'
            <tr> <td> <b> {n} </b> </td> </tr>
            """

            info = table.format(n = program["name"])


            # self.graphs[self.k]["name"] + '|'
            info += ' '.join(map(lambda x: '<tr><td>' + x["name"] + ':=' + x["value"] + '</td></tr>', program["var"]))
            info += "</table>>"


            # for i in self.graphs[self.k]["var"]:
            #     info += i["name"] + ':=' + i["value"] + '\\n'

            for i in program["state"]:
                start = i["start"]
                end = i["end"]
                condition = i["condition"]
                action = i["action"]
                condition_res = ""
                action_res = ""
                if start == 'entry':
                    print('entry{i}[shape=circle label="" style=filled color=black]'.format(i=ind), sep='', file=f)
                else:
                    print(start + '{i}[label="'.format(i=ind) + start.replace('"','\\"') + '"]', sep='', file=f)
                if end == 'exit':
                    print('exit{i}[shape=doublecircle label="" style=filled color=black]'.format(i=ind), sep='', file=f)
                else:
                    print(end + '{i}[label="'.format(i=ind) + end.replace('"','\\"') + '"]', sep='', file=f)

                if isinstance(condition, str):
                    condition_res = condition
                else:
                    condition_res = condition["name"] + '(' + ','.join(condition["value"]) + ')'
                if isinstance(action, str):
                    action_res = action
                else:
                    action_res = action["name"] + '(' + ','.join(action["value"]) + ')'
                sep = '/\\n'
                if condition_res == "" and action_res != "":
                    sep = '\\n/'
                if condition_res == "" and action_res == "":
                    sep = ''
                print(start +'{i}'.format(i=ind) + ' -> ' + end + '{i}'.format(i=ind) + '[label="' + (condition_res + sep + action_res).replace('"','\\"') + '"]', sep='', file=f)

            inner = ''.join(map(lambda x: '<tr><td>' +  x["name"] + '(' + ','.join(x["value"]) + ')' + '</td></tr>', program["inner"]))

            if inner != "":
                print('inner{i}[shape=none,label='.format(i=ind) + table.format(n="Inner") + inner + '</table>>];', sep='', file=f)

            print('info{i}[shape=none label='.format(i=ind) + info + ']', sep='', file=f)

            print("}", sep='', file=f)

            required = ''.join(map(lambda x: '<tr><td>' + x["name"] + '(' + ','.join(x["value"]) + ')' + '</td></tr>', program["required"]))
            if required != "":
                print('required{i}[shape=none,label='.format(i=ind) + table.format(n="Required") + required + '</table>>];', sep='', file=f)
                print('required{i} -> entry{i} [lhead=cluster{i} arrowtail=odot dir=back]'.format(i=ind), sep='', file=f)


            provided = ''.join(map(lambda x: '<tr><td>' + x["name"] + '(' + ','.join(x["value"]) + ')' + '</td></tr>', program["provided"]))
            if provided != "":
                print('provided{i}[shape=none,label='.format(i=ind) + table.format(n="Provided") + provided + '</table>>];', sep='', file=f)
                print('provided{i} -> entry{i} [lhead=cluster{i} arrowtail=icurve dir=back]'.format(i=ind), sep='', file=f)

        print("}", sep='', file=f)
        f.close()

    def get_graphs(self):
        return self.graphs

    # Visit a parse tree1 produced by ciaoParser#p.
    def visitP(self, ctx:ciaoParser.PContext):
        return self.visitChildren(ctx)


    # Visit a parse tree1 produced by ciaoParser#n.
    def visitN(self, ctx:ciaoParser.NContext):
        self.k += 1
        self.graphs.append({})
        self.graphs[self.k].clear()
        self.graphs[self.k]['name'] = ""
        self.graphs[self.k]['var'] = []
        self.graphs[self.k]['required'] = []
        self.graphs[self.k]['provided'] = []
        self.graphs[self.k]['inner'] = []
        self.graphs[self.k]['query'] = []
        self.graphs[self.k]['state'] = []

        self.graphs[self.k]['name'] = ctx.getChild(0).getText()
        return self.visitChildren(ctx)




    # Visit a parse tree1 produced by ciaoParser#v.
    def visitV(self, ctx:ciaoParser.VContext):
        n = ctx.getChildCount()
        i = 1
        while (i < n):
            self.graphs[self.k]['var'].append({
            'name': ctx.getChild(i).getText(),
            'value': self.visit(ctx.getChild(i + 2))})
            i += 3
        return self.visitChildren(ctx)


    # Visit a parse tree1 produced by ciaoParser#e.
    def visitE(self, ctx:ciaoParser.EContext):
        n = ctx.getChildCount()
        # print(n)
        i = 1
        while (i < n - 1):
            # print(ctx.getChild(i).getText(), ctx.getChild(i + 2))
            self.graphs[self.k]['required'].append({
            'name': ctx.getChild(i).getText(),
            'value': self.visit(ctx.getChild(i + 2))})
            i += 4
        return self.visitChildren(ctx)


    # Visit a parse tree1 produced by ciaoParser#a.
    def visitA(self, ctx:ciaoParser.AContext):
        n = ctx.getChildCount()
        # print(n)
        i = 1
        while (i < n - 1):
            # print(ctx.getChild(i).getText(), ctx.getChild(i + 2))
            self.graphs[self.k]['provided'].append({
            'name': ctx.getChild(i).getText(),
            'value': self.visit(ctx.getChild(i + 2))})
            i += 4
        return self.visitChildren(ctx)


    # Visit a parse tree1 produced by ciaoParser#r.
    def visitR(self, ctx:ciaoParser.RContext):
        n = ctx.getChildCount()
        # print(n)
        i = 1
        while (i < n - 1):
            # print(ctx.getChild(i).getText(), ctx.getChild(i + 2))
            self.graphs[self.k]['inner'].append({
            'name': ctx.getChild(i).getText(),
            'value': self.visit(ctx.getChild(i + 2))})
            i += 4
        return self.visitChildren(ctx)


    # Visit a parse tree1 produced by ciaoParser#q.
    def visitQ(self, ctx:ciaoParser.QContext):
        n = ctx.getChildCount()
        # print(n)
        i = 1
        while (i < n - 1):
            # print(ctx.getChild(i).getText(), ctx.getChild(i + 2))
            self.graphs[self.k]['query'].append({
            'name': ctx.getChild(i).getText(),
            'value': self.visit(ctx.getChild(i + 2))})
            i += 4
        return self.visitChildren(ctx)


    # Visit a parse tree1 produced by ciaoParser#u.
    def visitU(self, ctx:ciaoParser.UContext):
        n = ctx.getChildCount()
        # print(n)
        i = 1
        while (i < n):
            start = ctx.getChild(i).getText()
            condition = ""
            i += 2
            if (ctx.getChild(i).getText() != '/'):
                condition = self.visit(ctx.getChild(i))
                i += 1
            i += 1
            action = ""
            if (ctx.getChild(i).getText() != '->'):
                action = self.visit(ctx.getChild(i))
                i += 1
            i += 1
            end = ctx.getChild(i).getText()
            self.graphs[self.k]['state'].append({
            'start': start,
            'end': end,
            'condition': condition,
            'action': action
            })
            i += 1
        return self.visitChildren(ctx)


    # Visit a parse tree1 produced by ciaoParser#funcCondition.
    def visitFuncCondition(self, ctx:ciaoParser.FuncConditionContext):
        return {'name' : ctx.getChild(0).getText(),
                'value' : self.visit(ctx.getChild(2))}


    # Visit a parse tree1 produced by ciaoParser#exprCondition.
    def visitExprCondition(self, ctx:ciaoParser.ExprConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree1 produced by ciaoParser#exprAction.
    def visitExprAction(self, ctx:ciaoParser.ExprActionContext):
        return ctx.getChild(0).getText() + ':=' + self.visit(ctx.getChild(2))


    # Visit a parse tree1 produced by ciaoParser#funcAction.
    def visitFuncAction(self, ctx:ciaoParser.FuncActionContext):
        #x = self.visit(ctx.getChild(2))
        # print(x, type(x), ctx.getChild(2))
        #return ctx.getChild(0).getText() + '(' + ','.join(x) + ')'
        return {'name' : ctx.getChild(0).getText(),
                'value' : self.visit(ctx.getChild(2))}

    # Visit a parse tree1 produced by ciaoParser#func.
    def visitFunc(self, ctx:ciaoParser.FuncContext):
        return ctx.getChild(0).getText() + '(' + ','.join(self.visit(ctx.getChild(2))) + ')'


    # Visit a parse tree1 produced by ciaoParser#variables.
    def visitVariables(self, ctx:ciaoParser.VariablesContext):
        n = ctx.getChildCount()
        i = 0
        res = []
        while (i < n):
            # print(ctx.getChild(i).getText(), ctx.getChildCount())
            if (ctx.getChild(i).getText() != ","):
                res.append(ctx.getChild(i).getText())
            i += 1
        return res


    def visitValues(self, ctx:ciaoParser.ValuesContext):
        n = ctx.getChildCount()
        i = 0
        res = []
        # print('i', i, n)
        while (i < n):
            # print("ctx.getChild(i).getText()", ctx.getChild(i).getText() != ",")
            if (ctx.getChild(i).getText() != ","):
                res.append(self.visit(ctx.getChild(i)))
            i += 1
        return res


    # Visit a parse tree1 produced by ciaoParser#notExpr.
    def visitNotExpr(self, ctx:ciaoParser.NotExprContext):
        return 'not ' + self.visit(ctx.getChild(1))


    # Visit a parse tree1 produced by ciaoParser#unaryMinusExpr.
    def visitUnaryMinusExpr(self, ctx:ciaoParser.UnaryMinusExprContext):
        return '-' + self.visit(ctx.getChild(1))


    # Visit a parse tree1 produced by ciaoParser#atomExpr.
    def visitAtomExpr(self, ctx:ciaoParser.AtomExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree1 produced by ciaoParser#orExpr.
    def visitOrExpr(self, ctx:ciaoParser.OrExprContext):
        return self.visit(ctx.getChild(0)) + ' or ' + self.visit(ctx.getChild(2))


    # Visit a parse tree1 produced by ciaoParser#relationalExpr.
    def visitRelationalExpr(self, ctx:ciaoParser.RelationalExprContext):
        x = self.visit(ctx.getChild(2))
        return self.visit(ctx.getChild(0)) + ctx.getChild(1).getText() + x


    # Visit a parse tree1 produced by ciaoParser#equalityExpr.
    def visitEqualityExpr(self, ctx:ciaoParser.EqualityExprContext):
        return self.visit(ctx.getChild(0)) + ctx.getChild(1).getText() + self.visit(ctx.getChild(2))


    # Visit a parse tree1 produced by ciaoParser#andExpr.
    def visitAndExpr(self, ctx:ciaoParser.AndExprContext):
        return self.visit(ctx.getChild(0)) + ' and ' + self.visit(ctx.getChild(2))


    # Visit a parse tree1 produced by ciaoParser#parExpr.
    def visitParExpr(self, ctx:ciaoParser.ParExprContext):
        return '(' + self.visit(ctx.getChild(1)) + ')'


    # Visit a parse tree1 produced by ciaoParser#numberAtom.
    def visitNumberAtom(self, ctx:ciaoParser.NumberAtomContext):
        return ctx.getText()


    # Visit a parse tree1 produced by ciaoParser#booleanAtom.
    def visitBooleanAtom(self, ctx:ciaoParser.BooleanAtomContext):
        return ctx.getText()


    # Visit a parse tree1 produced by ciaoParser#idAtom.
    def visitIdAtom(self, ctx:ciaoParser.IdAtomContext):
        return ctx.getText()


    # Visit a parse tree1 produced by ciaoParser#stringAtom.
    def visitStringAtom(self, ctx:ciaoParser.StringAtomContext):
        return ctx.getText()


    # Visit a parse tree1 produced by ciaoParser#multiplicationExpr.
    def visitMultiplicationExpr(self, ctx:ciaoParser.MultiplicationExprContext):
        return self.visit(ctx.getChild(0)) + ctx.getChild(1).getText() + self.visit(ctx.getChild(2))


    # Visit a parse tree1 produced by ciaoParser#additiveExpr.
    def visitAdditiveExpr(self, ctx:ciaoParser.AdditiveExprContext):
        return self.visit(ctx.getChild(0)) + ctx.getChild(1).getText() + self.visit(ctx.getChild(2))


del ciaoParser
