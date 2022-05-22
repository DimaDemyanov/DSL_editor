const initialState = false;

export function SourceCodeFieldReducer(state = initialState, action) {
  console.log('Changing state: ' + action.type);
  switch(action.type) {
    case "WRITING_PROGRAM":
      return true;
    case "WRITING_GRAMMAR":
      return false;
    default:
      return state;
  }
}