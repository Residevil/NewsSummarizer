import React from "react";
import { Route, Switch } from "wouter";
import { AppLayout } from "../layout/AppLayout";
import { DigestsPage } from "../pages/DigestsPage";
import { SettingsPage } from "../pages/SettingsPage";
import { ModelsPage } from "../pages/ModelsPage";

export const Router: React.FC = () => {
  return (
    <AppLayout>
      <Switch>
        <Route path="/" component={DigestsPage} />
        <Route path="/settings" component={SettingsPage} />
        <Route path="/models" component={ModelsPage} />
        <Route>404 Not Found</Route>
      </Switch>
    </AppLayout>
  );
};
