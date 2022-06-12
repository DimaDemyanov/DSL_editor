function save(sourceCode, syntax, semantics) {
  localStorage.setItem('sourceCode', sourceCode);
  localStorage.setItem('syntax', syntax);
  localStorage.setItem('semantics', semantics);
}

export const LocalStorage = { save };
