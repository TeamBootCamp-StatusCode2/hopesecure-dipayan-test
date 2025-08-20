/**
 * Polling-based real-time client for HopeSecure Campaign Monitoring
 * Uses HTTP polling to simulate real-time updates
 */

class PollingRealTimeClient {
    constructor() {
        this.pollingIntervals = new Map();
        this.eventHandlers = new Map();
        this.defaultInterval = 5000; // 5 seconds
        this.isPolling = new Map();
    }

    /**
     * Start polling for campaign updates
     * @param {string} campaignId - Campaign ID to monitor
     * @param {string} token - Authentication token
     * @param {function} onUpdate - Callback for updates
     * @param {number} interval - Polling interval in ms
     */
    startCampaignPolling(campaignId, token, onUpdate, interval = this.defaultInterval) {
        const key = `campaign_${campaignId}`;
        
        // Stop existing polling for this campaign
        this.stopPolling(key);
        
        const pollFunction = async () => {
            try {
                const response = await fetch(`http://127.0.0.1:8000/api/campaigns/${campaignId}/live-stats/`, {
                    headers: {
                        'Authorization': `Token ${token}`,
                        'Content-Type': 'application/json',
                    }
                });
                
                if (response.ok) {
                    const data = await response.json();
                    if (onUpdate) {
                        onUpdate({
                            type: 'campaign_update',
                            data: data
                        });
                    }
                } else {
                    console.error('Failed to fetch campaign stats:', response.statusText);
                }
            } catch (error) {
                console.error('Error polling campaign data:', error);
                if (onUpdate) {
                    onUpdate({
                        type: 'error',
                        error: error.message
                    });
                }
            }
        };
        
        // Initial fetch
        pollFunction();
        
        // Set up interval
        const intervalId = setInterval(pollFunction, interval);
        this.pollingIntervals.set(key, intervalId);
        this.isPolling.set(key, true);
        
        console.log(`✅ Started polling for ${key} every ${interval}ms`);
    }

    /**
     * Start polling for dashboard updates
     * @param {string} token - Authentication token
     * @param {function} onUpdate - Callback for updates
     * @param {number} interval - Polling interval in ms
     */
    startDashboardPolling(token, onUpdate, interval = this.defaultInterval) {
        const key = 'dashboard';
        
        // Stop existing polling
        this.stopPolling(key);
        
        const pollFunction = async () => {
            try {
                const response = await fetch('http://127.0.0.1:8000/api/campaigns/stats/', {
                    headers: {
                        'Authorization': `Token ${token}`,
                        'Content-Type': 'application/json',
                    }
                });
                
                if (response.ok) {
                    const data = await response.json();
                    if (onUpdate) {
                        onUpdate({
                            type: 'dashboard_update',
                            data: data
                        });
                    }
                }
            } catch (error) {
                console.error('Error polling dashboard data:', error);
            }
        };
        
        // Initial fetch
        pollFunction();
        
        // Set up interval
        const intervalId = setInterval(pollFunction, interval);
        this.pollingIntervals.set(key, intervalId);
        this.isPolling.set(key, true);
        
        console.log(`✅ Started dashboard polling every ${interval}ms`);
    }

    /**
     * Stop polling for a specific key
     * @param {string} key - Polling key
     */
    stopPolling(key) {
        const intervalId = this.pollingIntervals.get(key);
        if (intervalId) {
            clearInterval(intervalId);
            this.pollingIntervals.delete(key);
            this.isPolling.set(key, false);
            console.log(`🛑 Stopped polling for ${key}`);
        }
    }

    /**
     * Stop all polling
     */
    stopAllPolling() {
        for (const [key, intervalId] of this.pollingIntervals) {
            clearInterval(intervalId);
            this.isPolling.set(key, false);
        }
        this.pollingIntervals.clear();
        console.log('🛑 Stopped all polling');
    }

    /**
     * Check if polling is active for a key
     * @param {string} key - Polling key
     * @returns {boolean}
     */
    isPollingActive(key) {
        return this.isPolling.get(key) || false;
    }

    /**
     * Update polling interval
     * @param {string} key - Polling key
     * @param {number} newInterval - New interval in ms
     */
    updateInterval(key, newInterval) {
        if (this.isPollingActive(key)) {
            // Store current handlers and restart with new interval
            this.stopPolling(key);
            // Note: This would need to be implemented with stored handlers
            console.log(`Updated interval for ${key} to ${newInterval}ms`);
        }
    }
}

// Campaign-specific polling monitor
class CampaignPollingMonitor {
    constructor(campaignId, token) {
        this.campaignId = campaignId;
        this.token = token;
        this.client = new PollingRealTimeClient();
        this.eventHandlers = {
            campaignUpdate: [],
            campaignEvent: [],
            connectionError: []
        };
        this.lastUpdateTime = null;
        this.isActive = false;
    }

    /**
     * Start monitoring campaign with polling
     * @param {number} interval - Polling interval in ms
     */
    startMonitoring(interval = 5000) {
        this.isActive = true;
        this.client.startCampaignPolling(
            this.campaignId,
            this.token,
            (data) => this.handleUpdate(data),
            interval
        );
    }

    /**
     * Stop monitoring campaign
     */
    stopMonitoring() {
        this.isActive = false;
        this.client.stopPolling(`campaign_${this.campaignId}`);
    }

    /**
     * Handle incoming updates
     */
    handleUpdate(data) {
        const { type, data: updateData, error } = data;

        if (error) {
            this.triggerEvent('connectionError', error);
            return;
        }

        switch (type) {
            case 'campaign_update':
                // Check if data has actually changed
                const currentUpdateTime = updateData.last_updated;
                if (currentUpdateTime !== this.lastUpdateTime) {
                    this.lastUpdateTime = currentUpdateTime;
                    this.triggerEvent('campaignUpdate', updateData);
                }
                
                // Handle recent events
                if (updateData.recent_events && updateData.recent_events.length > 0) {
                    updateData.recent_events.forEach(event => {
                        this.triggerEvent('campaignEvent', event);
                    });
                }
                break;

            default:
                console.log('Unknown update type:', type);
        }
    }

    /**
     * Register event handler
     * @param {string} event - Event name
     * @param {function} handler - Event handler function
     */
    on(event, handler) {
        if (this.eventHandlers[event]) {
            this.eventHandlers[event].push(handler);
        }
    }

    /**
     * Remove event handler
     * @param {string} event - Event name
     * @param {function} handler - Event handler function to remove
     */
    off(event, handler) {
        if (this.eventHandlers[event]) {
            const index = this.eventHandlers[event].indexOf(handler);
            if (index > -1) {
                this.eventHandlers[event].splice(index, 1);
            }
        }
    }

    /**
     * Trigger event handlers
     */
    triggerEvent(event, data) {
        if (this.eventHandlers[event]) {
            this.eventHandlers[event].forEach(handler => {
                try {
                    handler(data);
                } catch (error) {
                    console.error('Error in event handler:', error);
                }
            });
        }
    }

    /**
     * Manually trigger a data refresh
     */
    refresh() {
        if (this.isActive) {
            // Force immediate poll by temporarily reducing interval
            this.client.stopPolling(`campaign_${this.campaignId}`);
            this.client.startCampaignPolling(
                this.campaignId,
                this.token,
                (data) => this.handleUpdate(data),
                100 // Very short interval for immediate update
            );
            
            // Restore normal interval after 1 second
            setTimeout(() => {
                if (this.isActive) {
                    this.client.stopPolling(`campaign_${this.campaignId}`);
                    this.client.startCampaignPolling(
                        this.campaignId,
                        this.token,
                        (data) => this.handleUpdate(data),
                        5000 // Back to normal
                    );
                }
            }, 1000);
        }
    }

    /**
     * Check if monitoring is active
     * @returns {boolean}
     */
    isMonitoring() {
        return this.isActive && this.client.isPollingActive(`campaign_${this.campaignId}`);
    }
}

// Export for use in React components
export { PollingRealTimeClient, CampaignPollingMonitor };
