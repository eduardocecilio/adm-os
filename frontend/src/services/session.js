const USER_SCOPED_STORAGE_KEYS = [
    'token',
    'activeWorkspace',
    'userWorkspaces',
    'historico_balanco',
    'historico_dre'
];

export function clearUserSession() {
    USER_SCOPED_STORAGE_KEYS.forEach((key) => localStorage.removeItem(key));
}

export function startUserSession(token) {
    clearUserSession();
    localStorage.setItem('token', token);
}
