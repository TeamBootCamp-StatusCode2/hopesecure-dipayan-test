import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';
import { Button } from '../ui/button';
import { Progress } from '../ui/progress';
import { Badge } from '../ui/badge';
import { Alert, AlertDescription } from '../ui/alert';
import { 
    Play, 
    Pause, 
    Square, 
    Mail, 
    MousePointer, 
    KeyRound, 
    Download,
    Wifi,
    WifiOff,
    RefreshCw
} from 'lucide-react';
import { useCampaignRealTime } from '../../hooks/useRealTime';

interface CampaignControlPanelProps {
    campaignId: string;
    token: string;
    onCampaignAction?: (action: 'start' | 'pause' | 'stop', campaignId: string) => void;
}

export const CampaignControlPanel: React.FC<CampaignControlPanelProps> = ({
    campaignId,
    token,
    onCampaignAction
}) => {
    const {
        campaignData,
        events,
        isConnected,
        connectionError,
        requestStats
    } = useCampaignRealTime(campaignId, token);

    const handleCampaignAction = async (action: 'start' | 'pause' | 'stop') => {
        try {
            const response = await fetch(`http://127.0.0.1:8000/api/campaigns/${campaignId}/${action}/`, {
                method: 'POST',
                headers: {
                    'Authorization': `Token ${token}`,
                    'Content-Type': 'application/json',
                }
            });

            if (response.ok) {
                if (onCampaignAction) {
                    onCampaignAction(action, campaignId);
                }
                // Refresh stats after action
                setTimeout(() => requestStats(), 1000);
            } else {
                console.error(`Failed to ${action} campaign:`, await response.text());
            }
        } catch (error) {
            console.error(`Error ${action}ing campaign:`, error);
        }
    };

    if (!campaignData) {
        return (
            <Card className="w-full">
                <CardContent className="p-6">
                    <div className="flex items-center justify-center">
                        <RefreshCw className="h-6 w-6 animate-spin" />
                        <span className="ml-2">Loading campaign data...</span>
                    </div>
                </CardContent>
            </Card>
        );
    }

    const getStatusColor = (status: string) => {
        switch (status) {
            case 'active': return 'bg-green-500';
            case 'paused': return 'bg-yellow-500';
            case 'completed': return 'bg-blue-500';
            case 'stopped': return 'bg-red-500';
            default: return 'bg-gray-500';
        }
    };

    const getProgressPercentage = () => {
        if (!campaignData.target_count || campaignData.target_count === 0) return 0;
        return Math.round((campaignData.emails_sent / campaignData.target_count) * 100);
    };

    return (
        <div className="space-y-6">
            {/* Connection Status */}
            <Alert className={`${isConnected ? 'border-green-500' : 'border-red-500'}`}>
                <div className="flex items-center">
                    {isConnected ? (
                        <Wifi className="h-4 w-4 text-green-500" />
                    ) : (
                        <WifiOff className="h-4 w-4 text-red-500" />
                    )}
                    <AlertDescription className="ml-2">
                        {isConnected 
                            ? 'Real-time monitoring active' 
                            : connectionError 
                                ? `Connection error: ${connectionError.message || 'Unknown error'}`
                                : 'Connecting to real-time updates...'
                        }
                    </AlertDescription>
                </div>
            </Alert>

            {/* Campaign Control Panel */}
            <Card>
                <CardHeader>
                    <div className="flex items-center justify-between">
                        <div>
                            <CardTitle className="flex items-center">
                                <MousePointer className="h-5 w-5 mr-2" />
                                Campaign Control Panel
                            </CardTitle>
                            <CardDescription>
                                Monitor and control your phishing simulation campaign
                            </CardDescription>
                        </div>
                        <div className="flex items-center space-x-2">
                            <Badge 
                                variant="secondary" 
                                className={`${getStatusColor(campaignData.status)} text-white`}
                            >
                                {campaignData.status?.toUpperCase()}
                            </Badge>
                            <Button 
                                variant="outline" 
                                size="sm" 
                                onClick={requestStats}
                                disabled={!isConnected}
                            >
                                <RefreshCw className="h-4 w-4" />
                            </Button>
                        </div>
                    </div>
                </CardHeader>

                <CardContent className="space-y-6">
                    {/* Campaign Info */}
                    <div className="grid grid-cols-2 gap-4 text-sm">
                        <div>
                            <span className="text-blue-600 font-medium">Campaign Template</span>
                        </div>
                        <div>
                            <span className="text-blue-600 font-medium">Target Department</span>
                        </div>
                        <div>
                            <span className="text-blue-600 font-medium">Total Recipients</span>
                        </div>
                        <div>
                            <span className="text-blue-600">{campaignData.target_count || 1} employees</span>
                        </div>
                    </div>

                    {/* Email Delivery Progress */}
                    <div className="space-y-2">
                        <div className="flex justify-between items-center">
                            <span className="text-sm font-medium">Email Delivery Progress</span>
                            <span className="text-sm text-gray-500">
                                {campaignData.emails_sent || 0} / {campaignData.target_count || 1} sent
                            </span>
                        </div>
                        <Progress value={getProgressPercentage()} className="h-2" />
                        <span className="text-xs text-gray-500">{getProgressPercentage()}% complete</span>
                    </div>

                    {/* Action Buttons */}
                    <div className="flex space-x-2">
                        <Button
                            onClick={() => handleCampaignAction('start')}
                            disabled={campaignData.status === 'active' || !isConnected}
                            className="flex items-center"
                            variant="default"
                        >
                            <Play className="h-4 w-4 mr-2" />
                            Start
                        </Button>
                        <Button
                            onClick={() => handleCampaignAction('pause')}
                            disabled={campaignData.status !== 'active' || !isConnected}
                            className="flex items-center"
                            variant="outline"
                        >
                            <Pause className="h-4 w-4 mr-2" />
                            Pause
                        </Button>
                        <Button
                            onClick={() => handleCampaignAction('stop')}
                            disabled={campaignData.status === 'stopped' || campaignData.status === 'completed' || !isConnected}
                            className="flex items-center"
                            variant="destructive"
                        >
                            <Square className="h-4 w-4 mr-2" />
                            Stop Campaign
                        </Button>
                    </div>
                </CardContent>
            </Card>

            {/* Real-time Statistics */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <Card>
                    <CardContent className="p-4">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-2xl font-bold text-blue-600">
                                    {campaignData.emails_opened || 0}
                                </p>
                                <p className="text-xs text-gray-500">Emails Opened</p>
                                <p className="text-xs text-gray-400">
                                    {campaignData.open_rate ? `${campaignData.open_rate.toFixed(1)}%` : '0%'} open rate
                                </p>
                            </div>
                            <Mail className="h-8 w-8 text-blue-500" />
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardContent className="p-4">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-2xl font-bold text-yellow-600">
                                    {campaignData.links_clicked || 0}
                                </p>
                                <p className="text-xs text-gray-500">Links Clicked</p>
                                <p className="text-xs text-gray-400">
                                    {campaignData.click_rate ? `${campaignData.click_rate.toFixed(1)}%` : '0%'} click rate
                                </p>
                            </div>
                            <MousePointer className="h-8 w-8 text-yellow-500" />
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardContent className="p-4">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-2xl font-bold text-red-600">
                                    {campaignData.credentials_submitted || 0}
                                </p>
                                <p className="text-xs text-gray-500">Credentials Entered</p>
                                <p className="text-xs text-gray-400">
                                    {campaignData.success_rate ? `${campaignData.success_rate.toFixed(1)}%` : '0%'} compromise rate
                                </p>
                            </div>
                            <KeyRound className="h-8 w-8 text-red-500" />
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardContent className="p-4">
                        <div className="flex items-center justify-between">
                            <div>
                                <p className="text-2xl font-bold text-purple-600">
                                    {campaignData.attachments_downloaded || 0}
                                </p>
                                <p className="text-xs text-gray-500">Downloads</p>
                                <p className="text-xs text-gray-400">
                                    {campaignData.emails_sent > 0 
                                        ? `${((campaignData.attachments_downloaded || 0) / campaignData.emails_sent * 100).toFixed(1)}%` 
                                        : '0%'} download rate
                                </p>
                            </div>
                            <Download className="h-8 w-8 text-purple-500" />
                        </div>
                    </CardContent>
                </Card>
            </div>

            {/* Recent Events */}
            {events.length > 0 && (
                <Card>
                    <CardHeader>
                        <CardTitle className="text-lg">Recent Activity</CardTitle>
                        <CardDescription>
                            Live feed of campaign events
                        </CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="space-y-2 max-h-60 overflow-y-auto">
                            {events.slice(0, 10).map((event, index) => (
                                <div key={index} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                                    <div className="flex items-center space-x-2">
                                        <Badge variant="outline" className="text-xs">
                                            {event.event_type}
                                        </Badge>
                                        <span className="text-sm">{event.target_email}</span>
                                    </div>
                                    <span className="text-xs text-gray-500">
                                        {new Date(event.created_at).toLocaleTimeString()}
                                    </span>
                                </div>
                            ))}
                        </div>
                    </CardContent>
                </Card>
            )}
        </div>
    );
};
