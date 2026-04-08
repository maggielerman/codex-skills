import { useAppBridge } from "@shopify/app-bridge-react";

export function useOptionalAppBridge<T = unknown>(): T | null {
  try {
    return useAppBridge() as T;
  } catch {
    return null;
  }
}
