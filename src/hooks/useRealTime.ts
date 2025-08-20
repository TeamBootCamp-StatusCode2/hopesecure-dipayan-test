import { useState, useEffect, useRef, useCallback } from 'react';
import { CampaignPollingMonitor, PollingRealTimeClient } from '../lib/realtime';

/**
 * Custom hook for real-time campaign monitoring using polling
 * @param {string} campaignId - Campaign ID to monitor
 * @param {string} token - Authentication token
 * @returns {object} Real-time campaign data and controls
 */
export const useCampaignRealTime = (campaignId: string, token: string) => {
    const [campaignData, setCampaignData] = useState<any>(null);
    const [events, setEvents] = useState<any[]>([]);
    const [isConnected, setIsConnected] = useState(false);
    const [connectionError, setConnectionError] = useState<string | null>(null);
    const monitorRef = useRef<CampaignPollingMonitor | null>(null);

    const startMonitoring = useCallback(() => {
        if (!campaignId || !token) return;

        // Clean up existing monitor
        if (monitorRef.current) {
            monitorRef.current.stopMonitoring();
        }

        // Create new monitor
        const monitor = new CampaignPollingMonitor(campaignId, token);
        
        // Set up event handlers
        monitor.on('campaignUpdate', (data) => {
            setCampaignData(data);
            setIsConnected(true);
            setConnectionError(null);
        });

        monitor.on('campaignEvent', (eventData) => {
            setEvents(prev => [eventData, ...prev].slice(0, 50)); // Keep last 50 events
        });

        monitor.on('connectionError', (error) => {
            setConnectionError(error);
            setIsConnected(false);
        });

        // Start monitoring with 3 second polling
        monitor.startMonitoring(3000);
        monitorRef.current = monitor;
        
        // Set connected after a short delay to allow first poll
        setTimeout(() => setIsConnected(true), 500);
    }, [campaignId, token]);

    const stopMonitoring = useCallback(() => {
        if (monitorRef.current) {
            monitorRef.current.stopMonitoring();
            monitorRef.current = null;
            setIsConnected(false);
        }
    }, []);

    const requestStats = useCallback(() => {
        if (monitorRef.current) {
            monitorRef.current.refresh();
        }
    }, []);

    // Start monitoring when dependencies change
    useEffect(() => {
        startMonitoring();
        return () => stopMonitoring();
    }, [startMonitoring, stopMonitoring]);

    return {
        campaignData,
        events,
        isConnected,
        connectionError,
        startMonitoring,
        stopMonitoring,
        requestStats
    };
};

/**
 * Custom hook for dashboard real-time updates using polling
 * @param {string} token - Authentication token
 * @returns {object} Real-time dashboard data and controls
 */
export const useDashboardRealTime = (token: string) => {
    const [dashboardData, setDashboardData] = useState<any>(null);
    const [isConnected, setIsConnected] = useState(false);
    const [connectionError, setConnectionError] = useState<string | null>(null);
    const clientRef = useRef<PollingRealTimeClient | null>(null);

    const startMonitoring = useCallback(() => {
        if (!token) return;

        // Clean up existing client
        if (clientRef.current) {
            clientRef.current.stopPolling('dashboard');
        }

        // Create new client
        const client = new PollingRealTimeClient();
        
        client.startDashboardPolling(
            token,
            (data) => {
                if (data.type === 'dashboard_update') {
                    setDashboardData(data.data);
                    setIsConnected(true);
                    setConnectionError(null);
                }
            },
            5000 // 5 second polling
        );

        clientRef.current = client;
        
        // Set connected after a short delay
        setTimeout(() => setIsConnected(true), 500);
    }, [token]);

    const stopMonitoring = useCallback(() => {
        if (clientRef.current) {
            clientRef.current.stopPolling('dashboard');
            clientRef.current = null;
            setIsConnected(false);
        }
    }, []);

    const requestStats = useCallback(() => {
        // Force immediate refresh by stopping and restarting with short interval
        if (clientRef.current && token) {
            clientRef.current.stopPolling('dashboard');
            clientRef.current.startDashboardPolling(
                token,
                (data) => {
                    if (data.type === 'dashboard_update') {
                        setDashboardData(data.data);
                        setIsConnected(true);
                        setConnectionError(null);
                    }
                },
                100 // Very short interval for immediate update
            );
            
            // Restore normal interval after 1 second
            setTimeout(() => {
                if (clientRef.current) {
                    clientRef.current.stopPolling('dashboard');
                    clientRef.current.startDashboardPolling(
                        token,
                        (data) => {
                            if (data.type === 'dashboard_update') {
                                setDashboardData(data.data);
                            }
                        },
                        5000 // Back to normal
                    );
                }
            }, 1000);
        }
    }, [token]);

    // Start monitoring when dependencies change
    useEffect(() => {
        startMonitoring();
        return () => stopMonitoring();
    }, [startMonitoring, stopMonitoring]);

    return {
        dashboardData,
        isConnected,
        connectionError,
        startMonitoring,
        stopMonitoring,
        requestStats
    };
};

/**
 * Custom hook for admin monitoring real-time updates using polling
 * @param {string} token - Authentication token
 * @returns {object} Real-time admin data and controls
 */
export const useAdminMonitoringRealTime = (token: string) => {
    const [adminData, setAdminData] = useState<any>(null);
    const [alerts, setAlerts] = useState<any[]>([]);
    const [systemUpdates, setSystemUpdates] = useState<any[]>([]);
    const [isConnected, setIsConnected] = useState(false);
    const [connectionError, setConnectionError] = useState<string | null>(null);
    const clientRef = useRef<PollingRealTimeClient | null>(null);

    const startMonitoring = useCallback(() => {
        if (!token) return;

        // Clean up existing client
        if (clientRef.current) {
            clientRef.current.stopAllPolling();
        }

        // Create new client
        const client = new PollingRealTimeClient();
        
        // For admin monitoring, we can poll multiple endpoints
        // This is a simplified version - you could extend to poll admin-specific endpoints
        client.startDashboardPolling(
            token,
            (data) => {
                if (data.type === 'dashboard_update') {
                    // Transform dashboard data for admin view
                    setAdminData({
                        ...data.data,
                        timestamp: new Date().toISOString()
                    });
                    setIsConnected(true);
                    setConnectionError(null);
                }
            },
            10000 // 10 second polling for admin view
        );

        clientRef.current = client;
        
        // Set connected after a short delay
        setTimeout(() => setIsConnected(true), 500);
    }, [token]);

    const stopMonitoring = useCallback(() => {
        if (clientRef.current) {
            clientRef.current.stopAllPolling();
            clientRef.current = null;
            setIsConnected(false);
        }
    }, []);

    const requestStats = useCallback(() => {
        // Force immediate refresh for admin data
        if (clientRef.current && token) {
            clientRef.current.stopPolling('dashboard');
            clientRef.current.startDashboardPolling(
                token,
                (data) => {
                    if (data.type === 'dashboard_update') {
                        setAdminData({
                            ...data.data,
                            timestamp: new Date().toISOString()
                        });
                        setIsConnected(true);
                        setConnectionError(null);
                    }
                },
                100 // Very short interval for immediate update
            );
            
            // Restore normal interval
            setTimeout(() => {
                if (clientRef.current) {
                    clientRef.current.stopPolling('dashboard');
                    clientRef.current.startDashboardPolling(
                        token,
                        (data) => {
                            if (data.type === 'dashboard_update') {
                                setAdminData({
                                    ...data.data,
                                    timestamp: new Date().toISOString()
                                });
                            }
                        },
                        10000 // Back to normal
                    );
                }
            }, 1000);
        }
    }, [token]);

    // Start monitoring when dependencies change
    useEffect(() => {
        startMonitoring();
        return () => stopMonitoring();
    }, [startMonitoring, stopMonitoring]);

    return {
        adminData,
        alerts,
        systemUpdates,
        isConnected,
        connectionError,
        startMonitoring,
        stopMonitoring,
        requestStats
    };
};
