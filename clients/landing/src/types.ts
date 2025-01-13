export interface NavLink {
  content: string;
  href: string;
  active?: boolean;
}

export interface NavData {
  header: string;
  list: Array<NavLink>;
}
