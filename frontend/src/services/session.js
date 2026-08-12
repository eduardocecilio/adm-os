const USER_SCOPED_STORAGE_KEYS = [
    'activeWorkspace',
    'userWorkspaces',
    'historico_balanco',
    'historico_dre'
];

export function clearUserSession() {
    sessionStorage.removeItem('token');
    // Remove tokens written by older snapshots during the security migration.
    localStorage.removeItem('token');
    USER_SCOPED_STORAGE_KEYS.forEach((key) => localStorage.removeItem(key));
}

export function startUserSession(token) {
    clearUserSession();
    sessionStorage.setItem('token', token);
}

export function getSessionToken() {
    return sessionStorage.getItem('token');
}
