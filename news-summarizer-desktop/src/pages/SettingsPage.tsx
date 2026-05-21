import React, { useEffect, useState } from "react";
import { getSettings, saveSettings, Settings } from "../api/settings";
import { getModels, selectModel, Model } from "../api/models";
import { PageHeader } from "../components/PageHeader";
import { Button } from "../components/ui/Button";
import { Card } from "../components/ui/Card";
import { Input } from "../components/ui/Input";
import { Select } from "../components/ui/Select";
import { useToast } from "../components/toast/ToastContext";

export const SettingsPage: React.FC = () => {
  const [settings, setSettings] = useState<Settings | null>(null);
  const [models, setModels] = useState<Model[]>([]);
  const [saving, setSaving] = useState(false);
  const { showToast } = useToast();

  useEffect(() => {
    (async () => {
      const s = await getSettings();
      const m = await getModels();
      setSettings(s);
      setModels(m);
    })();
  }, []);

  if (!settings) return <p className="text-gray-500">Loading settings…</p>;

  return (
    <>
      <PageHeader title="Settings" />

      <Card>
        <div className="flex flex-col gap-4">
          <div>
            <label className="mb-1 block font-medium">Refresh Interval (minutes)</label>
            <Input
              type="number"
              value={settings.refresh_interval_minutes}
              onChange={(e) =>
                setSettings({
                  ...settings,
                  refresh_interval_minutes: Number(e.target.value),
                })
              }
            />
          </div>

          <div>
            <label className="mb-1 block font-medium">Active Model</label>
            <Select
              value={settings.model}
              onChange={(e) =>
                setSettings({
                  ...settings,
                  model: e.target.value,
                })
              }
            >
              {models.map((m) => (
                <option key={m.name} value={m.name}>
                  {m.name}
                </option>
              ))}
            </Select>
          </div>

          <Button
            disabled={saving}
            onClick={async () => {
              setSaving(true);
              await saveSettings(settings);
              await selectModel(settings.model);
              setSaving(false);
              showToast("Settings saved");
            }}
          >
            {saving ? "Saving…" : "Save Settings"}
          </Button>
        </div>
      </Card>
    </>
  );
};
