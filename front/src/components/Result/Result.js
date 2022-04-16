import React from 'react';
import Button from '@material-ui/core/Button';
import './Result.css';

export function Result(props) {


  return (
        <div className="container">
          <div className="row">
          <div className="button">
            <Button variant="contained" color="primary" onClick={props.onClickAST}>AST</Button>
          </div>
          <div className="button">
            <Button variant="contained" color="primary" onClick={props.onClickInterpreter}>INTERPRETER</Button>
          </div>
          <div className="button">
            <Button variant="contained" color="primary" onClick={props.onClickCode}>Code</Button>
          </div>
          <div className="button">
            <Button variant="contained" color="primary" onClick={props.onClickDiagram}>Diagram</Button>
          </div>
          </div>
          <div className="row error" id="errorMsg">
              {props.error.value}
          </div>
        </div>
      )
}
