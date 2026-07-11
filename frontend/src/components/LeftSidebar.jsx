import { useMemo, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

import {
  Box,
  Divider,
  IconButton,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography,
  Drawer,
  useTheme,
  useMediaQuery,
} from '@mui/material';

import MenuIcon from '@mui/icons-material/Menu';
import MedicalServicesIcon from '@mui/icons-material/MedicalServices';
import PeopleIcon from '@mui/icons-material/People';
import EventAvailableIcon from '@mui/icons-material/EventAvailable';
import HistoryIcon from '@mui/icons-material/History';
import AdminPanelSettingsIcon from '@mui/icons-material/AdminPanelSettings';
import SelfImprovementIcon from '@mui/icons-material/SelfImprovement';
import SpaIcon from '@mui/icons-material/Spa';
import FavoriteIcon from '@mui/icons-material/Favorite';
import ChatIcon from '@mui/icons-material/Chat';
import AutoGraphIcon from '@mui/icons-material/AutoGraph';
import LocalHospitalIcon from '@mui/icons-material/LocalHospital';
import NotificationsIcon from '@mui/icons-material/Notifications';
import PsychologyIcon from '@mui/icons-material/Psychology';
import CrisisAlertIcon from '@mui/icons-material/WarningAmber';
import BookOnlineIcon from '@mui/icons-material/BookOnline';
import FitnessCenterIcon from '@mui/icons-material/FitnessCenter';
import ArticleIcon from '@mui/icons-material/Article';
import AdminLogoutIcon from '@mui/icons-material/Logout';


import { authAPI } from '../api/api';

const drawerWidth = 280;

function SidebarLink({ to, label, icon, active, onClick }) {
  return (
    <ListItemButton selected={active} onClick={onClick} sx={{ py: 1 }}>
      <ListItemIcon sx={{ minWidth: 40 }}>{icon}</ListItemIcon>
      <ListItemText primary={label} />
    </ListItemButton>
  );
}

export default function LeftSidebar({ children }) {
  const navigate = useNavigate();
  const location = useLocation();
  const theme = useTheme();
  const isSm = useMediaQuery(theme.breakpoints.down('md'));

  const [mobileOpen, setMobileOpen] = useState(false);

  const isAuthenticated = localStorage.getItem('token') !== null;
  const username = localStorage.getItem('username') || '';
  const isStaff = localStorage.getItem('is_staff') === 'true';

  const items = useMemo(() => {
    // Medical
    const base = [
      { to: '/dashboard', label: 'Medical Dashboard', icon: <MedicalServicesIcon /> },
      { to: '/doctors', label: 'Doctors', icon: <PeopleIcon /> },
      { to: '/book-appointment', label: 'Book Appointment', icon: <EventAvailableIcon /> },
      { to: '/my-appointments', label: 'Appointment History', icon: <HistoryIcon /> },
    ];

    // Mental Health
    base.push(
      { to: '/mental-health', label: 'Mental Health Dashboard', icon: <PsychologyIcon /> },
      { to: '/counselors', label: 'Counselors', icon: <ChatIcon /> },
      { to: '/mood-tracker', label: 'Mood Tracker', icon: <SpaIcon /> },
      { to: '/assessments', label: 'Assessments', icon: <SelfImprovementIcon /> },
      { to: '/wellness-resources', label: 'Wellness Resources', icon: <ArticleIcon /> },
      { to: '/quotes', label: 'Motivational Quotes', icon: <FavoriteIcon /> },
      { to: '/self-care', label: 'Self Care Planner', icon: <FitnessCenterIcon /> },
      { to: '/journal', label: 'Journal', icon: <BookOnlineIcon /> },
      { to: '/crisis-support', label: 'Crisis Support', icon: <CrisisAlertIcon /> },
      { to: '/notifications', label: 'Notifications', icon: <NotificationsIcon /> },
      { to: '/analytics', label: 'Analytics', icon: <AutoGraphIcon /> }
    );

    // Admin
    if (isStaff) {
      base.push({ to: '/admin', label: 'Admin Dashboard', icon: <AdminPanelSettingsIcon /> });
      base.push({ to: '/admin/mental-health', label: 'Manage Mental Health', icon: <LocalHospitalIcon /> });
    }

    return base;
  }, [isStaff]);

  const handleLogout = () => {
    authAPI.logout();
    navigate('/login');
  };

  const drawerContent = (
    <Box sx={{ width: drawerWidth }} role="presentation">
      <Toolbar sx={{ px: 2, py: 1 }}>
        <Typography variant="h6" fontWeight={800} sx={{ lineHeight: 1.1 }}>
          Well-Being
        </Typography>
        <Typography variant="caption" display="block" sx={{ color: 'text.secondary' }}>
          {username ? `Hi, ${username}` : 'Support Platform'}
        </Typography>
      </Toolbar>

      <Divider />

      <List sx={{ px: 1 }}>
        {items.map((it) => (
          <SidebarLink
            key={it.to}
            to={it.to}
            label={it.label}
            icon={it.icon}
            active={location.pathname === it.to}
            onClick={() => {
              if (isSm) setMobileOpen(false);
              navigate(it.to);
            }}
          />
        ))}
      </List>

      <Divider />

      <Box sx={{ p: 2 }}>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
          Quick actions
        </Typography>
        <List sx={{ p: 0 }}>
          <ListItemButton onClick={handleLogout} sx={{ py: 1 }}>
            <ListItemIcon sx={{ minWidth: 40 }}>
              <AdminLogoutIcon />
            </ListItemIcon>
            <ListItemText primary="Logout" />
          </ListItemButton>
        </List>
      </Box>
    </Box>
  );

  if (!isAuthenticated) return null;

  return (
    <Box sx={{ display: 'flex' }}>
      {/* Mobile */}
      <Drawer
        variant={isSm ? 'temporary' : 'permanent'}
        open={isSm ? mobileOpen : true}
        onClose={() => setMobileOpen(false)}
        ModalProps={{ keepMounted: true }}
        sx={{
          '& .MuiDrawer-paper': {
            width: drawerWidth,
            boxSizing: 'border-box',
          },
        }}
      >
        {drawerContent}
      </Drawer>

      {/* Content */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 2,
          ml: isSm ? 0 : `${drawerWidth}px`,
          width: isSm ? '100%' : `calc(100% - ${drawerWidth}px)`,
        }}
      >
        {/* Mobile top bar */}
        {isSm && (
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
            <IconButton onClick={() => setMobileOpen(true)}>
              <MenuIcon />
            </IconButton>
            <Typography variant="subtitle1" fontWeight={700}>
              Well-Being Support
            </Typography>
          </Box>
        )}

        {children}
      </Box>
    </Box>
  );
}

