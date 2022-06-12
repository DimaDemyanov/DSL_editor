import React, { useState } from 'react';
import { styled } from '@mui/material/styles';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemAvatar from '@mui/material/ListItemAvatar';
import ListItemText from '@mui/material/ListItemText';
import Avatar from '@mui/material/Avatar';
import IconButton from '@mui/material/IconButton';
import Button from '@mui/material/Button';
import FolderIcon from '@mui/icons-material/Folder';
import DeleteIcon from '@mui/icons-material/Delete';
import { ListItemButton } from '@mui/material';
import Dialog from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogContentText from '@mui/material/DialogContentText';
import DialogTitle from '@mui/material/DialogTitle';
import TextField from '@mui/material/TextField';

import { useHistory } from 'react-router-dom';
import fetchPostJson, { fetchGet } from '../../utilities/Queries';

const SERVER_URL = process.env.REACT_APP_SERVER_URL;
const GET_PROJECTS_URL = `${SERVER_URL}/get-user-projects`;
const CREATE_PROJECT_URL = `${SERVER_URL}/create-project`;

const Demo = styled('div')(({ theme }) => ({
  backgroundColor: theme.palette.background.paper,
}));

let projectsState = null;

function ProjectsExplorer() {
  const history = useHistory();

  function onProjectSelect(projectName) {
    document.cookie = `project=${projectName}`;
    history.push('/editor');
  }

  // Лучше вынести в отдельный компонент.
  // Вообще старайся уменьшать компоненты, 
  // например если у тебя стейт (useState) меняет что-то только в одной маленькой части,
  // то просто вынеси эту часть со стейтом в компонент
  function Project(name, key) {
    return (
      <ListItem
        key={key}
        secondaryAction={(
          <IconButton edge="end" aria-label="delete">
            <DeleteIcon />
          </IconButton>
      )}
      >
        <ListItemButton onClick={() => onProjectSelect(name)}>
          <ListItemAvatar>
            <Avatar>
              <FolderIcon />
            </Avatar>
          </ListItemAvatar>
          <ListItemText
            primary={name}
          />
        </ListItemButton>
      </ListItem>
    );
  }

  const [projects, setProjects] = useState(projectsState);
  const [open, setOpen] = useState(false);
  const [newProjectName, setNewProjectName] = useState('');

  const generate = async () => {
    const request = await fetchGet(GET_PROJECTS_URL);

    const response = await request.json();
    console.log(`Projects list received: ${response}`);

    const map = response.projects.map((name) => Project(name, name));

    console.log(map);

    projectsState = map;

    setProjects(map);
  };

  const handleClickOpen = () => {
    setOpen(true);
    console.log('clickedd');
  };

  const handleClose = () => {
    setOpen(false);
  };

  const handleCreate = async () => {
    setOpen(false);

    document.cookie = `project=${newProjectName}`;
    const request = await fetchPostJson(CREATE_PROJECT_URL);

    const response = await request.json();
    console.log(`Project created: ${response}`);

    projectsState = null;

    history.push('/editor');
  };

  if (projectsState === null) {
    console.log('Generating...');
    generate();
  }

  return (
    <Demo className="project-explorer">
      <div className="projects-list-container">
        <List>
          {projects}
        </List>
      </div>

      <Dialog open={open} onClose={handleClose}>
        <DialogTitle>Add new project</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Please provide name of new project
          </DialogContentText>
          <TextField
            autoFocus
            margin="dense"
            id="name"
            label="Name"
            type="email"
            fullWidth
            variant="standard"
            onChange={(e) => {
              setNewProjectName(e.target.value);
            }}
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Cancel</Button>
          <Button onClick={handleCreate}>Create</Button>
        </DialogActions>
      </Dialog>

      <Button className="add-project-button" variant="contained" onClick={handleClickOpen}>Add Project</Button>
    </Demo>
  );
}

export default ProjectsExplorer;
