import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import IconButton from '@mui/material/IconButton';
import MenuIcon from '@mui/icons-material/Menu';
import AccountCircle from '@mui/icons-material/AccountCircle';
import MenuItem from '@mui/material/MenuItem';
import Menu from '@mui/material/Menu';

import { getCookieByName, deleteCookie } from '../../utilities/Queries'

import { useHistory } from "react-router-dom";

export default function MenuAppBar() {
  const [auth, setAuth] = React.useState(true);
  const [anchorEl, setAnchorEl] = React.useState(null);
  const [showMenuButton, setShowMenuButton] = React.useState(true);

  const history = useHistory();

  const toProjects = () => {
    deleteCookie('project')
    history.push('projects-explorer')
  }

  const handleMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    setAnchorEl(null);
    deleteCookie('username')
    deleteCookie('project')
    setAuth(false)

    history.push('/')
  };

  const menuButton = () => {
    if (getCookieByName('project')) {
        setShowMenuButton(true)
    } else {
        setShowMenuButton(false)
    }
  }

  return (
    <Box sx={{ flexGrow: 1 }}>
      <AppBar position="static">
        <Toolbar onChange={menuButton}>
          {showMenuButton && <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="menu"
            sx={{ mr: 2 }}
            onClick={toProjects}
          >
            <MenuIcon />
          </IconButton>}
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            {getCookieByName('project')}
          </Typography>
          {auth && (
            <div>
              <IconButton
                size="large"
                aria-label="account of current user"
                aria-controls="menu-appbar"
                aria-haspopup="true"
                onClick={handleMenu}
                color="inherit"
              >
                <AccountCircle />
                {getCookieByName('username')}
              </IconButton>
              <Menu
                id="menu-appbar"
                anchorEl={anchorEl}
                keepMounted
                open={Boolean(anchorEl)}
                onClose={handleClose}
              >
                <MenuItem onClick={handleLogout}>Logout</MenuItem>
              </Menu>
            </div>
          )}
        </Toolbar>
      </AppBar>
    </Box>
  );
}