import React from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { CheckCircle, Mail, Users, TrendingUp, X } from "lucide-react";

interface SuccessDialogProps {
  open: boolean;
  onClose: () => void;
  results?: {
    total_targets: number;
    successful_sends: number;
    failed_sends: number;
    success_rate: number;
    sender_email: string;
    domain_info?: {
      name: string;
    };
  };
}

const SuccessDialog: React.FC<SuccessDialogProps> = ({ open, onClose, results }) => {
  if (!results) return null;

  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="max-w-md mx-auto">
        <DialogHeader className="text-center space-y-4">
          <div className="mx-auto w-16 h-16 bg-green-100 rounded-full flex items-center justify-center">
            <CheckCircle className="w-8 h-8 text-green-600" />
          </div>
          <DialogTitle className="text-xl font-semibold text-gray-900">
            Campaign Launched Successfully!
          </DialogTitle>
        </DialogHeader>
        
        <div className="space-y-6 mt-6">
          {/* Quick Stats */}
          <div className="grid grid-cols-2 gap-4">
            <div className="text-center p-3 bg-blue-50 rounded-lg">
              <div className="flex items-center justify-center mb-1">
                <Mail className="w-4 h-4 text-blue-600 mr-1" />
                <span className="text-sm font-medium text-blue-600">Total Sent</span>
              </div>
              <div className="text-2xl font-bold text-blue-700">{results.total_targets}</div>
            </div>
            <div className="text-center p-3 bg-green-50 rounded-lg">
              <div className="flex items-center justify-center mb-1">
                <TrendingUp className="w-4 h-4 text-green-600 mr-1" />
                <span className="text-sm font-medium text-green-600">Success Rate</span>
              </div>
              <div className="text-2xl font-bold text-green-700">{results.success_rate}%</div>
            </div>
          </div>

          {/* Detailed Results */}
          <div className="space-y-3">
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center">
                <div className="w-2 h-2 bg-green-500 rounded-full mr-3"></div>
                <span className="text-sm font-medium text-gray-700">Successful Sends</span>
              </div>
              <Badge variant="secondary" className="bg-green-100 text-green-800">
                {results.successful_sends}
              </Badge>
            </div>
            
            {results.failed_sends > 0 && (
              <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                <div className="flex items-center">
                  <div className="w-2 h-2 bg-red-500 rounded-full mr-3"></div>
                  <span className="text-sm font-medium text-gray-700">Failed Sends</span>
                </div>
                <Badge variant="secondary" className="bg-red-100 text-red-800">
                  {results.failed_sends}
                </Badge>
              </div>
            )}
          </div>

          {/* Sender Info */}
          <div className="border-t pt-4">
            <div className="flex items-center justify-between text-sm">
              <span className="text-gray-600">Sender:</span>
              <span className="font-medium text-gray-900">{results.sender_email}</span>
            </div>
            {results.domain_info && (
              <div className="flex items-center justify-between text-sm mt-2">
                <span className="text-gray-600">Domain:</span>
                <span className="font-medium text-gray-900">{results.domain_info.name}</span>
              </div>
            )}
          </div>
        </div>

        <div className="flex justify-end mt-6">
          <Button onClick={onClose} className="bg-green-600 hover:bg-green-700">
            Continue
          </Button>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default SuccessDialog;
