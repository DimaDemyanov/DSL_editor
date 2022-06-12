import { createStore } from 'redux';

import { SourceCodeFieldReducer } from './reducers';

const store = createStore(SourceCodeFieldReducer);

export default store;
