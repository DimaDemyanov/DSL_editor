import { SourceCode } from "./SourceCode";
import { connect } from "react-redux";
import MapStateToProps from "./MapStateToProps";

export default connect(MapStateToProps) (SourceCode)