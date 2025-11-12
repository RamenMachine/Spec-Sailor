import React, { useState } from 'react';
import { Upload, FileText, Download, CheckCircle, AlertCircle } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Alert, AlertDescription } from '@/components/ui/alert';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [uploadResult, setUploadResult] = useState<any>(null);
  const [analysisResult, setAnalysisResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError(null);
      setUploadResult(null);
      setAnalysisResult(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setUploading(true);
    setError(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/upload`, {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Upload failed');
      }

      const data = await response.json();
      setUploadResult(data);
    } catch (err: any) {
      setError(err.message || 'Failed to upload file. Please check the format and try again.');
    } finally {
      setUploading(false);
    }
  };

  const handleAnalyze = async () => {
    if (!uploadResult) return;

    setAnalyzing(true);
    setError(null);

    try {
      const response = await fetch(
        `${API_BASE_URL}/api/v1/analyze/${uploadResult.upload_id}`,
        { method: 'POST' }
      );

      if (!response.ok) {
        throw new Error('Analysis failed');
      }

      const data = await response.json();
      setAnalysisResult(data);
    } catch (err) {
      setError('Failed to analyze data. Please try again.');
    } finally {
      setAnalyzing(false);
    }
  };

  const handleDownload = () => {
    if (!analysisResult) return;
    window.open(`${API_BASE_URL}/api/v1/download/${analysisResult.job_id}`, '_blank');
  };

  const handleReset = () => {
    setFile(null);
    setUploadResult(null);
    setAnalysisResult(null);
    setError(null);
  };

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-2">Upload Your Data</h1>
        <p className="text-muted-foreground">
          Get instant churn predictions for your app users
        </p>
      </div>

      {/* Step 1: Download Template */}
      <Card>
        <CardHeader>
          <CardTitle>Step 1: Download Template (Optional)</CardTitle>
          <CardDescription>
            Download our template to ensure your data is in the correct format
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex gap-4">
            <Button
              variant="outline"
              onClick={() => window.open(`${API_BASE_URL}/api/v1/template`, '_blank')}
            >
              <Download className="mr-2 h-4 w-4" />
              Download CSV Template
            </Button>
          </div>
          <div className="text-sm text-muted-foreground space-y-2">
            <p>Your data should include:</p>
            <ul className="list-disc list-inside space-y-1">
              <li><strong>user_id</strong> - Unique identifier for each user</li>
              <li><strong>event_timestamp</strong> - When the event occurred</li>
              <li><strong>event_type</strong> - Type of activity (prayer, session, etc.)</li>
              <li className="text-purple-400">⚡ More columns = Better predictions!</li>
            </ul>
          </div>
        </CardContent>
      </Card>

      {/* Step 2: Upload File */}
      <Card>
        <CardHeader>
          <CardTitle>Step 2: Upload Your File</CardTitle>
          <CardDescription>
            Upload CSV, Excel, or JSON file with your user activity data
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            <div className="border-2 border-dashed border-purple-500/50 rounded-lg p-8 text-center hover:border-purple-500 transition-colors">
              <Upload className="mx-auto h-12 w-12 text-purple-500 mb-4" />
              <input
                type="file"
                accept=".csv,.xlsx,.json"
                onChange={handleFileChange}
                className="hidden"
                id="file-upload"
              />
              <label htmlFor="file-upload" className="cursor-pointer">
                <Button variant="outline" asChild>
                  <span>Choose File to Upload</span>
                </Button>
              </label>
              <p className="mt-2 text-sm text-muted-foreground">
                Accepted formats: CSV, Excel (.xlsx), JSON
              </p>
              <p className="text-sm text-muted-foreground">Maximum size: 50 MB</p>
            </div>

            {file && (
              <Alert>
                <FileText className="h-4 w-4" />
                <AlertDescription>
                  Selected: <strong>{file.name}</strong> ({(file.size / 1024 / 1024).toFixed(2)} MB)
                </AlertDescription>
              </Alert>
            )}

            {file && !uploadResult && (
              <Button
                onClick={handleUpload}
                disabled={uploading}
                className="w-full"
              >
                {uploading ? 'Uploading...' : 'Upload & Validate'}
              </Button>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Step 3: Preview & Analyze */}
      {uploadResult && (
        <Card>
          <CardHeader>
            <CardTitle>Step 3: Preview Your Data</CardTitle>
            <CardDescription>Review your data before analysis</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <p className="text-sm text-muted-foreground">Total Events</p>
                <p className="text-2xl font-bold">{uploadResult.summary.total_events.toLocaleString()}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Unique Users</p>
                <p className="text-2xl font-bold">{uploadResult.summary.unique_users.toLocaleString()}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Date Range</p>
                <p className="text-sm font-medium">
                  {new Date(uploadResult.summary.date_range[0]).toLocaleDateString()} -
                  {new Date(uploadResult.summary.date_range[1]).toLocaleDateString()}
                </p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Event Types</p>
                <p className="text-sm font-medium">{uploadResult.summary.event_types.length} types</p>
              </div>
            </div>

            {uploadResult.validation.warnings.length > 0 && (
              <Alert>
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>
                  <strong>Warnings:</strong>
                  <ul className="list-disc list-inside mt-2">
                    {uploadResult.validation.warnings.map((warning: string, i: number) => (
                      <li key={i}>{warning}</li>
                    ))}
                  </ul>
                </AlertDescription>
              </Alert>
            )}

            {!analysisResult && (
              <Button
                onClick={handleAnalyze}
                disabled={analyzing}
                className="w-full"
              >
                {analyzing ? 'Analyzing...' : 'Analyze Data'}
              </Button>
            )}
          </CardContent>
        </Card>
      )}

      {/* Step 4: Results */}
      {analysisResult && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <CheckCircle className="h-6 w-6 text-green-500" />
              Analysis Complete!
            </CardTitle>
            <CardDescription>Your predictions are ready</CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div>
                <p className="text-sm text-muted-foreground">Total Users</p>
                <p className="text-2xl font-bold">{analysisResult.summary.total_users.toLocaleString()}</p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">High Risk</p>
                <p className="text-2xl font-bold text-red-500">
                  {analysisResult.summary.high_risk.toLocaleString()}
                </p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Medium Risk</p>
                <p className="text-2xl font-bold text-yellow-500">
                  {analysisResult.summary.medium_risk.toLocaleString()}
                </p>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">Low Risk</p>
                <p className="text-2xl font-bold text-green-500">
                  {analysisResult.summary.low_risk.toLocaleString()}
                </p>
              </div>
            </div>

            <div className="flex gap-4">
              <Button onClick={handleDownload} className="flex-1">
                <Download className="mr-2 h-4 w-4" />
                Download Results
              </Button>
              <Button
                variant="outline"
                onClick={handleReset}
                className="flex-1"
              >
                Upload New File
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Error Display */}
      {error && (
        <Alert variant="destructive">
          <AlertCircle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}
    </div>
  );
}
