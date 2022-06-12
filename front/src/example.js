const sourceCodeExample = `( [ + {shape=circle} ]

  < 0 {color=red} >
  ( [ A ] )

  < 1 >
  ( [ * ]

    < 0 >
    ( [ B ] )

    < 1 >
    ( [ C ] )
  )
)`;

const syntaxExample = `grammar ASTgrammar;
    t : '(' n (l t )* ')';
    n : '[' txt  (c )* ']';
    l : '<' txt  (c )* '>';
    c : '{' txt '=' txt '}';
    txt : SYMBOL ( SYMBOL)*;
    SPACE: [ \\t\\r\\n] -> skip;
    SYMBOL: ~( '(' | ')' | '[' | ']' | '<' | '>' | '{' | '}' );`;

const semanticsExample = `Tree
VAR
  entryTreeFlag := False
  exitTreeFlag := False
  tree := ""
  node := ""
  link := ""
REQUIRED
  nextNode(x)
  nextLink(x)
  popNodesStack()
  node.entryNode()
  node.ifExitNode()
  link.entryLink()
  link.ifExitLink()
PROVIDED
  entryTree()
  ifExitTree()
STATE
  entry -> entryTreeFlag / node := nextNode(tree) -> start_node
  start_node -> True / node.entryNode() -> end_node
  end_node -> node.ifExitNode() /  -> get_link
  get_link -> True / link := nextLink(tree) -> check_link
  check_link -> link != "" / link.entryLink() -> end_link
  end_link -> link.ifExitLink() /  -> get_link
  check_link -> else / popNodesStack() -> end_tree
  end_tree -> True / exitTreeFlag := True -> exit


Node
VAR
  entryNodeFlag := False
  exitNodeFlag := False
  node := ""
REQUIRED
  popLinkStack()
  pushNodesStack(x)
  sizeNodeStack()
PROVIDED
  entryNode()
  ifExitNode()
INNER
  printNode()
  printLink(link)
STATE
  entry -> entryNodeFlag / pushNodesStack(node) -> print_node
  print_node -> True / printNode() -> check_link
  check_link -> sizeNodesStack() > 1 / printLink(popLinkStack()) -> end_node
  end_node -> True / exitNodeFlag := True -> exit
  check_link -> else / exitNodeFlag := True -> exit


Link
VAR
  entryLinkFlag := False
  exitLinkFlag := False
  link := ""
  tree := ""
REQUIRED
  nextTree(x)
  pushLinkStack(link)
  tree.entryTree()
  tree.ifExitTree()
PROVIDED
  entryLink()
  ifExitLink()
STATE
  entry -> entryLinkFlag / pushLinkStack(link) -> get_tree
  get_tree -> True / tree := nextTree(link) -> start_tree
  start_tree -> True / tree.entryTree() -> end_tree
  end_tree -> tree.ifExitTree() / exitLinkFlag := True -> exit
`;
export { syntaxExample, semanticsExample, sourceCodeExample };
