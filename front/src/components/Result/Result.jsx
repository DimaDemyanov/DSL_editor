import React, { useState } from 'react';
import Button from '@material-ui/core/Button';
import './Result.css';
import { connect } from 'react-redux';
import MapStateToProps from './MapStateToProps';
import { ToggleButtonGroup } from '@mui/material';
import ToggleButton from '@mui/material/ToggleButton';

import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';

import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';

function ResultTemplate(props) {
  const [alignment, setAlignment] = useState('text');
  const [open, setOpen] = useState(false);

  const handleChange = (
    event: React.MouseEvent<HTMLElement>,
    newAlignment: string,
  ) => {
    if (newAlignment) {
      setAlignment(newAlignment);
      props.onChangeInputType(newAlignment);
    }
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleCreate = async () => {
    setOpen(false);
  };

  const handleClickOpen = () => {
    setOpen(true);
    console.log('clickedd');
  };

  return (
    <div className="buttons-container">
      <div className="editor-buttons-row">
        <ToggleButtonGroup
          className="button-group"
          color="error"
          orientation="vertical"
          value={alignment}
          exclusive
          onChange={handleChange}
        >
          <ToggleButton value="text">Text</ToggleButton>
          <ToggleButton value="markdown">MARKDOWN</ToggleButton>
        </ToggleButtonGroup>
        <Button className="add-project-button" variant="contained" onClick={handleClickOpen}>Upload handler</Button>
        <Dialog open={open} onClose={handleClose}>
          <DialogTitle>Upload handler</DialogTitle>
          <DialogContent>
            <DialogContentText>
              Please select handler type and choose file
            </DialogContentText>
            <FormControl fullWidth>
              <InputLabel id="demo-simple-select-label">Handler type</InputLabel>
              <Select
                // labelId="demo-simple-select-label"
                // id="demo-simple-select"
                label="Age"
                onChange={handleChange}
              >
                <MenuItem value={10}>Input Handler</MenuItem>
                <MenuItem value={20}>AST Handler</MenuItem>
                <MenuItem value={30}>Output hadnler</MenuItem>
              </Select>
            </FormControl>
            <Button
              variant="contained"
              component="label"
            >
              Upload File
              <input
                type="file"
                hidden
              />
            </Button>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleClose}>Cancel</Button>
            <Button onClick={handleCreate}>Upload</Button>
          </DialogActions>
        </Dialog>
        <div className="buttons-block">
          <div className="button set-grammar-button">
            <Button variant="contained" color="primary" disabled={!props.changingGrammarActive} onClick={props.onClickSetGrammar}>Set grammar</Button>
          </div>
          <div className="button change-grammar-button">
            <Button variant="contained" color="primary" disabled={props.changingGrammarActive} onClick={props.onClickChangeGrammar}>Change grammar</Button>
          </div>
          <div className="button">
            <Button variant="contained" color="primary" disabled={props.changingGrammarActive} onClick={props.onClickSyntaxDiagram}>Syntax diagram</Button>
          </div>
        </div>

        <div className="buttons-block">
          <div className="button">
            <Button variant="contained" color="primary" disabled={props.changingGrammarActive} onClick={props.onClickAST}>AST</Button>
          </div>
          <div className="button">
            <Button variant="contained" color="primary" disabled={props.changingGrammarActive} onClick={props.onClickInterpreter}>INTERPRETER</Button>
          </div>
          <div className="button">
            <Button variant="contained" color="primary" disabled={props.changingGrammarActive} onClick={props.onClickCode}>Code</Button>
          </div>
          <div className="button">
            <Button variant="contained" color="primary" disabled={props.changingGrammarActive} onClick={props.onClickDiagram}>Diagram</Button>
          </div>
        </div>
      </div>
      <div className="row-error" id="errorMsg">
        {props.error.value}
      </div>
    </div>
  );
}

export default connect(MapStateToProps)(ResultTemplate);
