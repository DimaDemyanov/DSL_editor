import { connect } from 'react-redux';
import { SourceCode } from './SourceCode';

function MapStateToProps(state) {
  return ({
    style: !state ? { background: '#FFFFFF' } : { background: '#A9A9A9' },
    readOnly: state,
    highlightActiveLine: !state,
    value: localStorage.getItem('syntax'),
  });
}

export default connect(MapStateToProps)(SourceCode);
