import { deprecatedUrlSource, paymentSourceMap, type PaymentGateway } from '@/config/envConfig';

export function paymentAgentBySource(source: string | undefined): PaymentGateway | undefined {
  if (!source) return undefined;
  return paymentSourceMap[source.trim().toLowerCase()];
}

export function buildCheckoutPath(source: string, taskId: string): string {
  return `/c/${source}/${taskId}/`;
}

export function buildCheckoutSuccessPath(source: string, taskId: string): string {
  return `/c/${source}/${taskId}/success/`;
}

export function buildCheckoutSuccessUrl(source: string, taskId: string): string {
  return `${window.location.origin}${buildCheckoutSuccessPath(source, taskId)}`;
}

/** Source устаревших адресов, только если такой код есть в карте. */
export function deprecatedCheckoutSource(): string | undefined {
  if (!paymentAgentBySource(deprecatedUrlSource)) return undefined;
  return deprecatedUrlSource;
}
