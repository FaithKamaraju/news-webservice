import Link from "next/link";
import {
  ActionIcon,
  Badge,
  Button,
  Card,
  Group,
  Image,
  Text,
} from "@mantine/core";
import classes from "./NewsCardLarge.module.css";

export default function NewsCardLarge(props: { data: CardData }) {
  const {
    uuid,
    title,
    description,
    snippet,
    url,
    image_url,
    published_at,
    source,
    categories,
  } = props.data;

  return (
    <Link href={`/articles/${uuid}`}>
      <Card withBorder radius="md" p="md" className={classes.card}>
        <Card.Section>
          <Image
            src={image_url}
            alt={title}
            height={180}
            fallbackSrc="https://placehold.co/600x400?text=Placeholder"
          />
        </Card.Section>

        <Card.Section className={classes.section} mt="md">
          <Group justify="apart">
            <Text fz="lg" fw={500}>
              {title}
            </Text>
            <Badge size="sm" variant="light">
              {source}
            </Badge>
          </Group>
          <Text fz="sm" mt="xs">
            {description}
          </Text>
        </Card.Section>

        <Card.Section className={classes.section}>
          <Text mt="md" className={classes.label} c="dimmed">
            Perfect for you, if you enjoy
          </Text>
          <Group gap={7} mt={5}>
            {categories.map((category) => (
              <Badge key={category} size="sm" variant="outline">
                {category}
              </Badge>
            ))}
          </Group>
        </Card.Section>
      </Card>
    </Link>
  );
}
