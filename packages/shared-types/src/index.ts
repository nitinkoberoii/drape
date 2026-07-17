/** Standard response envelope used by Drape HTTP services. */
export interface ApiResponse<T> {
  data: T;
}

export interface HealthStatus {
  status: 'ok';
}
