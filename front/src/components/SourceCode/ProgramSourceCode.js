import { SourceCode } from "./SourceCode";
import { connect } from "react-redux";

function MapStateToProps (state) {
    return ({
        style: state ? {background: '#FFFFFF'} : {background: '#A9A9A9'},
        readOnly: !state,
        highlightActiveLine: state,
        value: localStorage.getItem("sourceCode")
    })
}

export default connect(MapStateToProps) (SourceCode)