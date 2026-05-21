import React, { useEffect, useState } from "react";
import { getModels, downloadModel, deleteModel, selectModel, Model } from "../api/models";
import { PageHeader } from "../components/PageHeader";
import { Button } from "../components/ui/Button";
import { Card } from "../components/ui/Card";
import { useToast } from "../components/toast/ToastContext";

export const ModelsPage: React.FC = () => {
  const [models, setModels] = useState<Model[]>([]);
  const [loading, setLoading] = useState(true);
  const { showToast } = useToast();

  async function load() {
    setLoading(true);
    const list = await getModels();
    setModels(list);
    setLoading(false);
  }

  useEffect(() => {
    load();
  }, []);

  return (
    <>
      <PageHeader title="Model Manager" />

      {loading && <p className="text-gray-500">Loading models…</p>}

      <div className="flex flex-col gap-4">
        {models.map((m) => (
          <Card key={m.name}>
            <h3 className="text-lg font-medium">{m.name}</h3>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              {m.installed ? "Installed" : "Not installed"}
            </p>

            <div className="mt-3 flex gap-2">
              {!m.installed && (
                <Button
                  onClick={async () => {
                    await downloadModel(m.name);
                    load();
                    showToast(`Model "${m.name}" downloaded.`);
                  }}
                >
                  Download
                </Button>
              )}

              {m.installed && (
                <Button
                  variant="danger"
                  onClick={async () => {
                    await deleteModel(m.name);
                    load();
                    showToast(`Model "${m.name}" deleted.`);
                  }}
                >
                  Delete
                </Button>
              )}

              <Button
                variant="ghost"
                onClick={async () => {
                  await selectModel(m.name);
                  showToast(`Selected model: ${m.name}`);
                }}
              >
                Select
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </>
  );
};
